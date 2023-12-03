import nba_api_helpers as nba
from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime, timezone
from dateutil.parser import parse
import pytest


@pytest.fixture
def daily_game():
    # Generate first game of the day
    test_board = scoreboard.ScoreBoard()
    test_games = test_board.games.get_dict()
    return test_games[0]


def test_get_team_ids():
    warriors_id = 1610612744
    lakers_id = 1610612747
    assert nba.get_team_ids(["warriors", "lakers"]) == [warriors_id, lakers_id]


def test_get_players_id():
    lebron_id = 2544
    stephen_curry_id = 201939
    luka_id = 1629029
    durant_id = 201142
    assert nba.get_player_ids(["lebron", "stephen curry", "luka", "durant"]) == [
        lebron_id,
        stephen_curry_id,
        luka_id,
        durant_id,
    ]


def test_get_todays_scoreboard(daily_game):
    games, _ = nba.get_todays_scoreboard()
    assert games[0] == daily_game
