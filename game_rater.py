from win_prediction_model import get_comeback_score
from config import FAVORITE_PLAYERS, HIGH_SCORER
import nba_api_helpers as nba
from yt_api import get_recent_NBA_videos


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


def get_games_recap(games: list):
    """
    Given a list of games, recap the game and determine if it is worth watching
    """

    # Get tonight's highlight clips from NBA youtube channel
    youtube_highlights = get_recent_NBA_videos()

    for i, game in enumerate(games):
        away_team = game["awayTeam"]["teamName"].upper()
        home_team = game["homeTeam"]["teamName"].upper()
        game_title = "{awayTeam} at {homeTeam}".format(
            awayTeam=away_team, homeTeam=home_team
        )
        print("Game {game_count}: ".format(game_count=i + 1) + game_title)

        # Check game status
        game_status = game["gameStatus"]
        if game_status == 1:  # Game has not started
            (
                game_time,
                hour_left_til_game_start,
                minute_left_til_game_start,
            ) = nba.get_time_til_game_start(game)
            if hour_left_til_game_start > 0:
                print(
                    f"Starts in {hour_left_til_game_start} hours {minute_left_til_game_start} minutes at {game_time.strftime('%I:%M %p')}"
                )
            else:
                print(
                    f"Starts in {minute_left_til_game_start} minutes at {game_time.strftime('%I:%M %p')}"
                )
        elif game_status == 2:  # Game in progress
            print("Game is currently in progress")
        elif (
            game_status == 3
        ):  # Game has finished. Determine if game is worth watching. Return highligh url if it is worth watching
            worth_watching = rate_game(game)
            # if game is worth watching, return highlight url
            url = ""
            if worth_watching:
                print("Game finished and is worth watching")
                for video in youtube_highlights:
                    video_title = video["snippet"]["title"]
                    if game_title in video_title or (
                        away_team in video_title and home_team in video_title
                    ):
                        url = (
                            "https://www.youtube.com/watch?v="
                            + video["snippet"]["resourceId"]["videoId"]
                        )
                        print("Highlight Links: " + url)
                        break
                if not url:
                    print(
                        "No highlight video found. Link to NBA Youtube Channel: https://www.youtube.com/@NBA/videos"
                    )
            else:
                print(
                    "Skip game. Not worth watching. Score: {} - {}".format(
                        game["awayTeam"]["score"], game["homeTeam"]["score"]
                    )
                )
        print("\n")
