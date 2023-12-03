from win_prediction_model import get_comeback_score
from config import FAVORITE_PLAYERS, HIGH_SCORER
import nba_api_helpers as nba


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


def game_leaders_is_fav_player(game: dict) -> bool:
    """
    Return true if a favorite player is a game leader
    """
    favorite_players_ids = nba.get_player_ids(FAVORITE_PLAYERS)

    for player in favorite_players_ids:
        if (
            player == game["gameLeaders"]["awayLeaders"]["personId"]
            or player == game["gameLeaders"]["homeLeaders"]["personId"]
        ):
            return True
    return False


def game_has_high_scorer(game: dict) -> bool:
    """
    Return true if the game has a player that scored a lot of points
    """
    if (
        game["gameLeaders"]["awayLeaders"]["points"] >= HIGH_SCORER
        or game["gameLeaders"]["homeLeaders"]["points"] >= HIGH_SCORER
    ):
        return True
    return False


def rate_game(game: dict) -> bool:
    """
    Given a game, rate the game and determine if it is worth watching.
    """
    worth_watching = (
        is_comeback(game)
        or is_close_game(game)
        or entered_ot(game)
        or game_leaders_is_fav_player(game)
        or game_has_high_scorer(game)
    )
    return worth_watching
