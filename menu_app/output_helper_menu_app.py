from datetime import datetime, timezone
from dateutil.parser import parse
import nba_api_helpers as nba
from game_rater import rate_game


def get_highlight_video_url(game, highlights):
    """
    Find a game's highlight video from the Youtube Channel
    """
    away_team = game["awayTeam"]["teamName"].upper()
    home_team = game["homeTeam"]["teamName"].upper()

    url = None
    for video in highlights:
        video_title = video["snippet"]["title"]
        if away_team in video_title and home_team in video_title:
            url = (
                "https://www.youtube.com/watch?v="
                + video["snippet"]["resourceId"]["videoId"]
            )
            break

    return url


def get_time_til_game_start(game: str):
    """
    Given a game starting time, calculate hours left til game start
    """
    game_time = parse(game["gameTimeUTC"])
    game_time_localized = game_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
    current_time = datetime.now(timezone.utc)
    time_difference = game_time_localized - current_time
    hour_difference = time_difference.days * 24 + time_difference.seconds // 3600
    minute_difference = (time_difference.seconds // 60) % 60

    if hour_difference > 0:
        return f"Starts at {game_time_localized.strftime('%I:%M %p')}"

    else:
        return f"Starts at {game_time_localized.strftime('%I:%M %p')}"


def get_todays_date():
    scoreboard = nba.get_todays_scoreboard()
    return scoreboard.score_board_date


def get_games_to_rate():
    """
    Get list of games to rate. Determined by user's favorite team
    """
    interesting_games = nba.get_interesting_game()

    if interesting_games != []:
        games = interesting_games
    else:
        all_games_today = nba.get_all_games_playing_today()
        games = all_games_today

    return games


def get_game_title(game):
    away_team = game["awayTeam"]["teamName"].upper()
    home_team = game["homeTeam"]["teamName"].upper()
    game_title = "{awayTeam} at {homeTeam}".format(
        awayTeam=away_team, homeTeam=home_team
    )
    return game_title


def get_game_rating(game):
    output = ""

    # Check game status
    game_status = game["gameStatus"]
    if game_status == 1:  # Game has not started
        output += get_time_til_game_start(game)
    elif game_status == 2:  # Game in progress
        output += "Game is currently in progress."
    elif game_status == 3:  # Game has finished
        worth_watching = rate_game(game)
        if worth_watching:
            output += "Worth watching."
        else:
            output += "Skip game. Score: {} - {}".format(
                game["awayTeam"]["score"], game["homeTeam"]["score"]
            )
    return output
