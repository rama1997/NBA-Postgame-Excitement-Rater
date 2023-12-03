from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams, players
from config import FAVORITE_TEAMS

todays_scoreboard = scoreboard.ScoreBoard()


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


def get_all_games_playing_today():
    """
    Return list of NBA games being played today
    """
    todays_games = todays_scoreboard.games.get_dict()
    return todays_games


def get_interesting_game():
    # Get interested teams
    favorite_teams_ids = get_team_ids(FAVORITE_TEAMS)

    # Get interested games from all games being played today
    all_games_today = get_all_games_playing_today()
    interesting_games = [
        game
        for game in all_games_today
        if game["awayTeam"]["teamId"] in favorite_teams_ids
        or game["homeTeam"]["teamId"] in favorite_teams_ids
    ]
    return interesting_games
