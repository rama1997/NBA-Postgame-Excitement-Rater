from win_prediction_model import get_comeback_score
import config


def is_close_game(game: dict) -> bool:
    """
    Return true if end of game score differed by less than 10
    """
    return abs(game["awayTeam"]["score"] - game["homeTeam"]["score"]) <= 10


def entered_ot(game: dict) -> bool:
    """
    Return true if game entered OT
    """
    return game["period"] > 4


def is_comeback(game: dict) -> bool:
    """
    Return true if there was a comeback in the 4th quarter or if the overall comeback score is high
    """
    comeback_score = get_comeback_score(game)
    print(f"Comeback Score: {comeback_score}")

    home_score_entering_fourth_q = (
        game["homeTeam"]["score"] - game["homeTeam"]["periods"][3]["score"]
    )

    away_score_entering_fourth_q = (
        game["awayTeam"]["score"] - game["awayTeam"]["periods"][3]["score"]
    )

    team_leading_entering_fourth_q = (
        game["awayTeam"]["teamId"]
        if away_score_entering_fourth_q > home_score_entering_fourth_q
        else game["homeTeam"]["teamId"]
    )

    winner = (
        game["awayTeam"]["teamId"]
        if game["awayTeam"]["score"] > game["homeTeam"]["score"]
        else game["homeTeam"]["teamId"]
    )

    score_difference_entering_fourth_q = abs(
        home_score_entering_fourth_q - away_score_entering_fourth_q
    )

    return (
        True
        if (
            team_leading_entering_fourth_q != winner
            and score_difference_entering_fourth_q > 10
        )
        or comeback_score >= 4
        else False
    )


def game_leaders_is_fav_player(game: dict, fav_players: list) -> bool:
    """
    Return true if an interested player is a game leader
    """
    for player in fav_players:
        if (
            player == game["gameLeaders"]["awayLeaders"]["personId"]
            or player == game["gameLeaders"]["homeLeaders"]["personId"]
        ):
            return True
    if (
        game["gameLeaders"]["awayLeaders"]["points"] >= config.HIGH_SCORER
        or game["gameLeaders"]["homeLeaders"]["points"] >= config.HIGH_SCORER
    ):
        return True
    return False


def rate_game(game: dict, fav_players: list) -> bool:
    """
    Given a game, rate the game and determine if it is worth watching.
    """
    worth_watching = (
        is_close_game(game)
        or is_comeback(game)
        or entered_ot(game)
        or game_leaders_is_fav_player(game, fav_players)
    )
    if worth_watching:
        print("Game finished and is worth watching")
        return True
    else:
        print(
            "Skip game. Not worth watching. Score: {} - {}".format(
                game["awayTeam"]["score"], game["homeTeam"]["score"]
            )
        )
        return False
