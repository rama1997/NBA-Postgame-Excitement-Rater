from nba_api_helpers import (
    get_team_ids,
    get_player_ids,
    get_todays_scoreboard,
    recap_games,
)
import config

if __name__ == "__main__":
    # Get interested teams
    favorite_teams = get_team_ids(config.FAVORITE_TEAMS)

    # Get interested players
    favorite_players = get_player_ids(config.FAVORITE_PLAYERS)

    # Get interested all_games from all all_games being played today
    all_games, board = get_todays_scoreboard()
    interested_games = [
        game
        for game in all_games
        if game["awayTeam"]["teamId"] in favorite_teams
        or game["homeTeam"]["teamId"] in favorite_teams
    ]

    # Get recaps of today's game
    print("Date: " + board.score_board_date + "\n")
    if interested_games != []:
        recap_games(interested_games, favorite_players)
    else:
        print("No interesting games today. Here is all the games from today:")
        recap_games(all_games, favorite_players)
