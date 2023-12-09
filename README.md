# NBA-Game-Recap

Determines whether or not a daily NBA games is "exciting" enough to watch by using game data obtained from the NBA API.

For games that are determined to be worth watching, search for the highlight video from the offical NBA Youtube channel using the Youtube API.

Aims to give a spoiler free decision on whether or not you should watch the game highlights for those that don't have time to watch the full NBA game

## Preview:
<img src="https://i.imgur.com/hZdKpEu.png" width="450" height="300" />
<img src="https://i.imgur.com/32kdesI.png" width="680" height="206" />


## Features
- Uses the NBA API to obtain the daily game schedule as well as the game’s result and stats
- Evaluates the play by play and post game stats in order to determines whether a game is exciting enough to watch or not
- Allows user to pick specific teams/players that they want to track rather than every daily game
- Recieve the highlight reel of each game from the offical NBA Youtube channel using the Youtube API
- Option of running as a menu bar app in MacOS built from `rumps`. Note: Still a work in progress


## Win Prediction Model
Built and implemented a win prediction model in order to have a more accurate representation of whether or not a game was close or consisted of a comeback.

Model Details:
- Instead of building one model for the entire game, 5 seperate model were built in order to represent the first, second, third, and fourth quarter as well as overtime
- Each model was a locally weighted Logistic Regression Model using the LOESS method
- Models were trained on historical play by play data and results for all regular season and playoff NBA games over the last 15 years(2007-2022) obtained from the NBA API 
- Win probability is calculate as a function of game time and the score difference
- Model assumes a 50/50 model meaning both team are evenly matches and playing on a neutral court which removes home court advantage. Does not take into account historical team nor player performance.
- Model had a 75% accuracy when predicting the winning team

Steps used to build my models can be found in the `model` folder

# Installation and Set up
## Prerequisites
- Python
- Pip 
- Set up Google Cloud App wth Oauth2 Desktop App credential for Youtube API 

First, download from Github onto your computer
```
git clone https://github.com/rama1997/NBA-Postgame-Excitement-Rater.git
cd NBA-Postgame-Excitement-Rater
```

Clone this repo and install packages listed in `requirements.txt`

```
pip install -r requirements.txt
```

You may want to install the requirements in a Python virtual environment to ensure they don't conflict with other Python projects on your system.

## Configuration
Configure `config.py` with the desired data

- Include favorite teams/players to search for
- Set minimum point count to be considered as a high scorer

Example included in `config.py`

## Usage
Run 
```
python3 main.py
```

Using the experimental menu bar 
```
python3 main.py --menu
```
Clicking on a finished game from the menu bar will open up the highlight video in your browser.

## Todo:
- Retrain model to include possession of ball when calculating win probability
- Improve how a close game is determined. How close the game stayed at the 50/50 probability
