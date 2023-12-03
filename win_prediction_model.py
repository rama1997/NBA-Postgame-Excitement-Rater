import pickle
import datetime
import time
import requests
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import playbyplay
import warnings

# Remove FutureWarning of deprecated sklearn version
warnings.simplefilter(action="ignore", category=FutureWarning)


def run_model(game):
    game = pd.DataFrame(game)

    # Split game into quarters
    q1 = game.loc[game["TIME_REMAINING"] >= 2160]
    q2 = game.loc[(game["TIME_REMAINING"] >= 1440) & (game["TIME_REMAINING"] <= 2160)]
    q3 = game.loc[(game["TIME_REMAINING"] >= 720) & (game["TIME_REMAINING"] <= 1440)]
    q4 = game.loc[
        (game["TIME_REMAINING"] >= 0)
        & (game["TIME_REMAINING"] <= 720)
        & (game["OT"] == 0)
    ]
    ot = game.loc[game["OT"] == 1]

    # Load each quarter specific model
    q1_model = pickle.load(open("./model/q1_model.sav", "rb"))
    q2_model = pickle.load(open("./model/q2_model.sav", "rb"))
    q3_model = pickle.load(open("./model/q3_model.sav", "rb"))
    q4_model = pickle.load(open("./model/q4_model.sav", "rb"))
    ot_model = pickle.load(open("./model/ot_model.sav", "rb"))

    # Run model on game data
    q1_p = q1_model.predict_proba(
        q1[["TIME_REMAINING", "HOME_SCORE", "AWAY_SCORE", "SCORE_MARGIN", "OT"]]
    ).tolist()
    q2_p = q2_model.predict_proba(
        q2[["TIME_REMAINING", "HOME_SCORE", "AWAY_SCORE", "SCORE_MARGIN", "OT"]]
    ).tolist()
    q3_p = q3_model.predict_proba(
        q3[["TIME_REMAINING", "HOME_SCORE", "AWAY_SCORE", "SCORE_MARGIN", "OT"]]
    ).tolist()
    q4_p = q4_model.predict_proba(
        q4[["TIME_REMAINING", "HOME_SCORE", "AWAY_SCORE", "SCORE_MARGIN", "OT"]]
    ).tolist()

    # Obtain predictions
    predictions = q1_p + q2_p + q3_p + q4_p

    # Do the same for OT if game entered OT
    if len(ot) > 0:
        ot_p = ot_model.predict_proba(
            ot[["TIME_REMAINING", "HOME_SCORE", "AWAY_SCORE", "SCORE_MARGIN", "OT"]]
        ).tolist()
        predictions += ot_p

    # Returns prediction
    return predictions


# Retry Wrapper to avoid timing out when calling API
def retry(func, retries=3):
    def retry_wrapper(*args, **kwargs):
        attempts = 0
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(30)
                attempts += 1

    return retry_wrapper


@retry
def get_game_play_by_play(game):
    # Get play by play data
    pbp = playbyplay.PlayByPlay(game["gameId"]).get_data_frames()[0]

    # Get desired data for model training. Setting up columns GAME_ID, AWAY_SCORE, HOME_SCORE, SCORE_MARGIN, HOME_WIN, OT
    res = pd.DataFrame()
    res["GAME_ID"] = pbp["GAME_ID"].astype(str)
    res["SCORE"] = pbp["SCORE"].copy()

    # Edit SCORE to eliminate empty scores
    prev_score = "0 - 0"
    for i in range(len(res)):
        play = res.iloc[[i]]
        if res.loc[i, "SCORE"] == None:
            res.loc[i, "SCORE"] = prev_score
        else:
            prev_score = res.loc[i, "SCORE"]

    # Split SCORE into AWAY_SCORE and HOME_SCORE
    res[["AWAY_SCORE", "HOME_SCORE"]] = (
        res["SCORE"].str.split("-", expand=True).astype(int)
    )
    res.drop("SCORE", axis=1, inplace=True)

    # Set up SCORE_MARGIN to remove 'TIE' and None values
    res["SCORE_MARGIN"] = pbp["SCOREMARGIN"].copy()
    prev_margin = "0"
    for i in range(len(res)):
        play = res.iloc[[i]]
        if res.loc[i, "SCORE_MARGIN"] == None:
            res.loc[i, "SCORE_MARGIN"] = prev_margin
        elif res.loc[i, "SCORE_MARGIN"] == "TIE":
            res.loc[i, "SCORE_MARGIN"] = "0"
            prev_margin = "0"
        else:
            prev_margin = res.loc[i, "SCORE_MARGIN"]
    res["SCORE_MARGIN"] = res["SCORE_MARGIN"].astype(int)

    # Set up HOME_WIN based on SCOREMARGIN
    res["HOME_WIN"] = 1 if int(pbp.tail(1)["SCOREMARGIN"].values[0]) > 0 else 0
    res["OT"] = 0

    # lambda function that converts the PCTIMESTRING to seconds using datetime
    time_to_seconds = (
        lambda x: datetime.datetime.strptime(x, "%M:%S").minute * 60
        + datetime.datetime.strptime(x, "%M:%S").second
    )
    res["TIME_REMAINING"] = ((4 - pbp["PERIOD"]) * 12 * 60) + pbp["PCTIMESTRING"].apply(
        time_to_seconds
    )

    # Handling time remaining for overtime
    res.loc[res["TIME_REMAINING"] < 0, "OT"] = 1
    res.loc[res["TIME_REMAINING"] < 0, "TIME_REMAINING"] = pbp["PCTIMESTRING"].apply(
        time_to_seconds
    )

    return res


def get_comeback_score(game):
    # Get game's play by play data. Catch ValueError if game is finished, but stats are not uploaded yet
    try:
        play_by_play = get_game_play_by_play(game)
    except ValueError:
        return -1

    # Run model on the game to obtain win probabilities at each play
    model_results = run_model(
        play_by_play[
            ["TIME_REMAINING", "HOME_SCORE", "AWAY_SCORE", "SCORE_MARGIN", "OT"]
        ]
    )

    # Make predictions more coherant by adding 100% win probablity at the end of the game to winning team. Calculate lowest win probably of the winning team
    lowest_win_prob = 1
    if game["homeTeam"]["score"] > game["awayTeam"]["score"]:
        predictions = np.append(model_results, [[0, 1]], axis=0)
        for p in predictions:
            lowest_win_prob = min(lowest_win_prob, p[1])
    else:
        predictions = np.append(model_results, [[1, 0]], axis=0)
        for p in predictions:
            lowest_win_prob = min(lowest_win_prob, p[0])

    # Returns odds of winning at lowest probability as comeback score
    return (1 - lowest_win_prob) / lowest_win_prob
