# NBA-Game-Recap

Determines whether or not a daily NBA games is "exciting" enough to watch by using live data obtained from the NBA API. For games that are determined to be worth watching, we will search for the highlight video from the offical NBA Youtube channel using the Youtube API.

## Preview:
<img src="https://i.imgur.com/hZdKpEu.png" width="450" height="300" />

## Features
- Uses the NBA API to obtain the daily game schedule as well as the game’s result and stats
- Evaluates the play by play and post game stats in order to determines whether a game is exciting enough to watch or not
- Allows user to pick specific teams/players that they want to track rather than every daily game
- Uses the Youtube API to recieve the highlight reel of each game from the offical NBA Youtube channel

## Win Prediction Model
Implemented a win prediction model in order to have a more accurate representation of whether or not a game was close or consisted of a comeback.

Model Details:
- Instead of building one model for the entire game, 5 seperate model were built in order to represent the first, second, third, and fourth quarter as well as overtime
- Each model was a locally weighted Logistic Regression Model using the LOESS method
- Models were trained on historical play by play data and results for all regular season and playoff NBA games over the last 15 years(2007-2022) obtained from the NBA API 
- Win probability is calculate as a function of game time and the score difference
- Model assumes a 50/50 model meaning both team are evenly matches and playing on a neutral court which removes home court advantage. Does not take into account historical team nor player performance.

Steps used to build my models can be found in the `model` folder

## Usage
Configure `config.py` with the desired data

- Requires credential for Youtube API
- Include favorite teams/players to search for
- Set minimum point count to be considered as a high scorer

Example included in `config.py`

## Todo:
- Improve how a close game is determined. How close the game stayed at the 50/50 probability
