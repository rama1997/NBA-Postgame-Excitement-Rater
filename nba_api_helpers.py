from datetime import datetime, timezone
from dateutil.parser import parse
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams, players


def get_todays_scoreboard():
    """
    Return list of NBA games being played today
    """
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()
    return games, board


def get_team_ids(teams_to_find: list[str]) -> list[int]:
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
    return game_time_localized, hour_difference, minute_difference
