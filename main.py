import nba_api_helpers as nba
from output_helper import print_output


if __name__ == "__main__":
    all_games_today = nba.get_all_games_playing_today()
    interesting_games = nba.get_interesting_game()

    # Get recaps of today's game
    if interesting_games != []:
        print_output(interesting_games)
    else:
        print("No personally interesting games today. Showing all games from today:\n")
        print_output(all_games_today)
