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
    Return true if there was a comeback in the 4th quarter
    """
    comeback_score = get_comeback_score(game)
    #print(f"Comeback Score: {comeback_score} %")
    leading_entering_fourth = (
        game["awayTeam"]["teamId"]
        if game["awayTeam"]["score"] - game["awayTeam"]["periods"][3]["score"]
        > game["homeTeam"]["score"] - game["homeTeam"]["periods"][3]["score"]
        else game["homeTeam"]["teamId"]
    )
    winner = (
        game["awayTeam"]["teamId"]
        if game["awayTeam"]["score"] > game["homeTeam"]["score"]
        else game["homeTeam"]["teamId"]
    )
    return not (leading_entering_fourth == winner)


def interesting_game_leaders(game: dict, fav_players: list) -> bool:
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
    Checks if it was a close game, it game entered OT, if there was a comeback, and if a interested player was game leader
    """
    comeback_score = is_comeback(game)
    worth_watching = (
        is_close_game(game)
        or entered_ot(game)
        or interesting_game_leaders(game, fav_players)
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
