from datetime import datetime, timezone
from dateutil.parser import parse
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams, players
from yt_api import get_videos_from_playlist
from game_rater import rate_game


def get_todays_scoreboard():
    """
    Return list of NBA games being played today
    """
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()
    return games, board


def get_team_ids(teams_to_find: list[str]) -> list[str]:
    """
    Given a list of team names, return a list of the team's id
    """
    ids = []
    for team in teams_to_find:
        try:
            team_data = teams.find_teams_by_full_name(team)
            team_id = team_data[0]["id"]
            ids.append(team_id)
        except Exception as _:
            print('Team "{}" not found'.format(team))
    return ids


def get_player_ids(players_to_find: list[str]) -> list[str]:
    """
    Given a list of player names, return a list of the  player's id
    """
    ids = []
    for player in players_to_find:
        try:
            player_data = players.find_players_by_full_name(player)
            player_id = player_data[0]["id"]
            ids.append(player_id)
        except Exception as _:
            print('Player "{}" not found'.format(player))
    return ids


def time_til_game_start(game_time: str):
    """
    Given a game starting time, calculate hours left til game start
    """
    game_time_localized = game_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
    current_time = datetime.now()
    diff = game_time_localized.hour - current_time.hour
    if diff > 0:
        print("{} hours til game starts.".format(diff))
    elif diff == 0:
        print("Starts in less than an hour")


def recap_games(games: list, favorite_players: list):
    """
    Given a list of games, recap the game and determine if it is worth watching
    """

    # Get tonight's highlight clips from NBA youtube channel
    youtube_highlights = get_videos_from_playlist(
        "NBA", "Nightly Full Game Highlights | 2022-23"
    )

    for i, game in enumerate(games):
        away_team = game["awayTeam"]["teamName"].upper()
        home_team = game["homeTeam"]["teamName"].upper()
        game_title = "{awayTeam} at {homeTeam}".format(
            awayTeam=away_team, homeTeam=home_team
        )
        print("Game {game_count}: ".format(game_count=i + 1) + game_title)

        # Check game status
        if (
            game["gameStatus"] == 1
        ):  # Game has not started -> show time remaining til start
            time_til_game_start(parse(game["gameTimeUTC"]))
        elif game["gameStatus"] == 2:  # Game in progress
            print("Game is currently in progress")
        elif (
            game["gameStatus"] == 3
        ):  # Game has finished. Determine if game is worth watching. Return highligh url if it is worth watching
            worth_watching = rate_game(game, favorite_players)
            # if game is worth watching, return highlight url
            url = ""
            if worth_watching:
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
                    print("No highlight video found.")
        print("\n")
