import nba_api_helpers as nba
from game_rater import get_games_recap
from config import FAVORITE_TEAMS

if __name__ == "__main__":
    # Get interested teams
    favorite_teams_ids = nba.get_team_ids(FAVORITE_TEAMS)

    # Get interested games from all games being played today
    all_games, board = nba.get_todays_scoreboard()
    interested_games = [
        game
        for game in all_games
        if game["awayTeam"]["teamId"] in favorite_teams_ids
        or game["homeTeam"]["teamId"] in favorite_teams_ids
    ]

    # Get recaps of today's game
    print("Date: " + board.score_board_date + "\n")
    if interested_games != []:
        get_games_recap(interested_games)
    else:
        print("No personally interesting games today. Showing all games from today:\n")
        get_games_recap(all_games)
