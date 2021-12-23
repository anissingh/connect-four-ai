"""CSC111 Winter 2021 Final Project: The Main Module

Module Description
===============================
This Python module is the main module of this project. It imports the necessary functions that are
required for running and displaying interactive Connect Four Games.

Copyright Information
===============================
This file is Copyright (c) 2021 Anis Singh.
"""
from runner import run_game_two, run_game, run_games_ai

if __name__ == '__main__':
    """
    IMPORTANT: If you are on a Mac, make sure the pygame window is selected before you quit it!
    In my experience on my Mac, the pygame display window will stop responding if it is quit
    when it is unselected. This has not yet happened to me when on my windows computer. I strongly
    believe that this does not have to do with how I handle quitting events, as this occurred 
    on my Mac when using course-provided code to close pygame windows (e.g., in tutorials 9 and 10).
    """

    """
    Function #1: run_game
    
    Play a game of Connect Four against an AI that uses the minimax algorithm. The user is always
    red and the AI is always yellow.
    
    Parameters:
      - d: determines the depth that AI uses the minimax algorithm to
      - red_starts: determines the player that starts the game
      
    Below are a few example calls to this function. For more information, see the docstring of
    this function (found in the runner.py module).
    """
    run_game(d=5, red_starts=False)
    # run_game(d=4, red_starts=True)
    # run_game(d=2, red_starts=False)

    """
    Function #2: run_games_ai
    
    Watch an AI that uses the minimax algorithm (yellow player) play against an AI that makes
    purely random moves (red player). Statistics are reported as described in the project report.
    
    Parameters:
      - n: the total number of games that will be played
      - d: determines the depth that minimax AI uses the minimax algorithm to
      - rand_starts: determines if the random AI starts or not
      
    Below are a few example calls to this function. For more information, see the docstring of
    this function (found in the runner.py module).
    """
    # run_games_ai(n=5, d=4, rand_starts=False)
    # run_games_ai(n=5, d=3, rand_starts=True)

    """
    Function #3: run_game_two (for fun)
    
    Play a two-player game of Connect Four.
    
    Parameters:
      - red_starts: determines the player that starts the game
      
    Below is an example call to this function. For more information, see the docstring of
    this function (found in the runner.py module).
    """
    # run_game_two(red_starts=True)
