from dateutil.parser import parse
import game_rater
from yt_api import get_videos_from_playlist
import nba_api_helpers

# Get interested teams
interested_teams = ['warriors','lakers','suns', 'nuggets', '76']
interested_teams = nba_api_helpers.get_team_ids(interested_teams)

# Get interested players
interested_players = ['booker', 'giannis', 'Shai', 'anthony Davis', 'stephen curry', 'klay']
interested_players = nba_api_helpers.get_player_ids(interested_players)

# Get interested games from all games being played today
games, board= nba_api_helpers.get_todays_scoreboard()
interested_games = [game for game in games if game['awayTeam']['teamId'] in interested_teams or game['homeTeam']['teamId'] in interested_teams]

# Set score for player to be considered high scorer
highscore = 50

# Get recaps of today's game
print("Date: " + board.score_board_date + "\n")
if interested_games != []:
	nba_api_helpers.recap_games(interested_games, interested_players, highscore)
else:
	print("No interesting games today. Here is all the games from today:")
	nba_api_helpers.recap_games(games, interested_players, highscore)

