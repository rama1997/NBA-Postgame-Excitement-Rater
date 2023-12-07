from datetime import datetime, timezone
from dateutil.parser import parse
import nba_api_helpers as nba
from yt_api import get_recent_NBA_videos
from game_rater import rate_game


def get_highlight_video_url(home_team: str, away_team: str, highlights) -> str:
    """
    Find a game's highlight video from the Youtube Channel
    """
    url = None
    for video in highlights:
        video_title = video["snippet"]["title"]
        if away_team in video_title and home_team in video_title:
            url = (
                "https://www.youtube.com/watch?v="
                + video["snippet"]["resourceId"]["videoId"]
            )
            break

    if url:
        return "Highlight Links: " + url
    if not url:
        return "No highlight video found. Check NBA Youtube Channel: https://www.youtube.com/@NBA/videos"


def get_time_til_game_start(game: str) -> str:
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
        return f"Starts in {hour_difference} hours {minute_difference} minutes at {game_time.strftime('%I:%M %p')}"
    else:
        return (
            f"Starts in {minute_difference} minutes at {game_time.strftime('%I:%M %p')}"
        )


def get_games_to_rate():
    """
    Get list of games to rate. Determined by user's favorite team
    """
    interesting_games = nba.get_interesting_game()

    if interesting_games != []:
        games = interesting_games
    else:
        print("No personally interesting games today. Showing all games from today:\n")
        all_games_today = nba.get_all_games_playing_today()
        games = all_games_today

    return games


def print_output():
    """
    Given a list of games, recap the game and determine if it is worth watching
    """

    scoreboard = nba.get_todays_scoreboard()
    print("Date: " + scoreboard.score_board_date + "\n")

    games = get_games_to_rate()

    youtube_highlights = (
        get_recent_NBA_videos()
    )  # Get tonight's highlight clips from NBA youtube channel

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
            print(get_time_til_game_start(game))
        elif game_status == 2:  # Game in progress
            print("Game is currently in progress")
        elif game_status == 3:  # Game has finished
            worth_watching = rate_game(game)
            if worth_watching:
                print("Game finished and is worth watching. Highlight video:")
                print(get_highlight_video_url(home_team, away_team, youtube_highlights))
            else:
                print(
                    "Skip game. Not worth watching. Score: {} - {}".format(
                        game["awayTeam"]["score"], game["homeTeam"]["score"]
                    )
                )
        print("\n")
