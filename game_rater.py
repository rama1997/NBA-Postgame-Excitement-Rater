'''
Functions to rate the NBA game
'''

def rate_game(game: {}, players: [], highscore:int ) -> bool:
	"""
	Given a game, rate the game and determine if it is worth watching.
	Checks if it was a close game, it game entered OT, if there was a comeback, and if a interested player was game leader
	"""
	worth_watching = is_close_game(game) or entered_ot(game) or comeback(game) or high_scorer(game, highscore) or interested_game_leaders(game, players)
	if worth_watching:
		print("Game finished and is worth watching")
		return True
	else:
		print('Skip game. Not worth watching. Score: {} - {}'.format(game['awayTeam']['score'], game['homeTeam']['score']))
		return False

def is_close_game(game: {}) -> bool:
	"""
	Return true if end of game score differed by less than 10
	"""
	return abs(game['awayTeam']['score'] - game['homeTeam']['score']) <= 10

def entered_ot(game: {}) -> bool:
	"""
	Return true if game entered OT
	"""
	return game['period'] > 4

def comeback(game: {}) -> bool:
	"""
	Return true if there was a comeback in the 4th quarter
	"""
	lead = game['awayTeam']['teamId'] if game['awayTeam']['score'] - game['awayTeam']['periods'][3]['score'] > game['homeTeam']['score']-game['homeTeam']['periods'][2]['score'] else game['homeTeam']['teamId']
	winner = game['awayTeam']['teamId'] if game['awayTeam']['score'] > game['homeTeam']['score'] else game['homeTeam']['teamId']
	return not(lead==winner)

def interested_game_leaders(game: {}, players: []) -> bool:
	"""
	Return true if an interested player is a game leader
	"""
	for player in players:
		if player == game['gameLeaders']['awayLeaders']['personId'] or player == game['gameLeaders']['homeLeaders']['personId']:
			return True
	return False

def high_scorer(game: {}, highscore: int) -> bool:
	"""
	Return true if a player scored a certain amount of points
	"""
	if game['gameLeaders']['awayLeaders']['points'] >= highscore or game['gameLeaders']['homeLeaders']['points'] >= highscore:
		return True
	return False