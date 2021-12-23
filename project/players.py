"""CSC111 Winter 2021 Final Project: Connect Four Players Module

Module Description
===============================
This Python module contains that govern the functionality of a player in a Connect Four game;
specifically, the functionality of allowing a user or an AI to make a move in a game. It contains
classes representing different AI's that make moves using different algorithms, as well as a
function that allows a user to make a move.

Copyright Information
===============================
This file is Copyright (c) 2021 Anis Singh.
"""
from typing import Optional
import random
import time
import game_tree
from connect_four import ConnectFourGame


def user_make_move(game: ConnectFourGame, previous_move: Optional[int], move: int) -> Optional[int]:
    """Make <move> in the given Connect Four game, and return the move made. If the move was
    invalid and no move was made, return <previous_move>.

    Preconditions:
        - There is at least one valid move for the given game

    >>> connect_game = ConnectFourGame()
    >>> connect_game.is_red_move()
    True
    >>> user_make_move(game=connect_game, previous_move=None, move=3)
    3
    >>> connect_game.is_red_move()
    False
    >>> user_make_move(game=connect_game, previous_move=3, move=0)
    0
    >>> connect_game.get_board()
    array([[0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0.],
           [2., 0., 0., 1., 0., 0., 0.]])
    """
    try:
        game.make_move(move)
        return move
    except ValueError:
        return previous_move


class PlayerAI:
    """An abstract class that represents a Connect Four Player.

    This class is heavily inspired by the PlayerAI class from Assignment 2. The handout for this
    assignment can be found here:
    https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/a2/handout/
    """

    def make_move(self, game: ConnectFourGame, previous_move: Optional[int]) -> int:
        """Make a move in the given Connect Four game.

        <previous_move> is the opponent's most recent move, or None if no moves have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        raise NotImplementedError


class RandomPlayer(PlayerAI):
    """A Connect Four AI Player that randomly chooses a move on each turn."""

    def make_move(self, game: ConnectFourGame, previous_move: Optional[int]) -> int:
        """Choose and make a random valid move in the given Connect Four game. Return the move
        that was made.

        <previous_move> is the opponent's most recent move, or None if no moves have been made.

        Wait 0.5 seconds before making the move.

        Preconditions:
           - There is at least one valid move for the given game
        """
        time.sleep(0.5)
        move = random.choice(game.get_valid_moves())
        game.make_move(move)
        return move


class MinimaxPlayer(PlayerAI):
    """A Connect Four AI Player that makes moves by using the minimax algorithm to a certain
    depth.
    """
    # Private Instance Attributes:
    #  -_depth: the depth that this AI uses in the minimax algorithm
    _depth: int

    def __init__(self, depth: int) -> None:
        """Initialize a new MinimaxPlayer that uses the minimax algorithm to the given depth.

        Preconditions:
            - depth > 0
        """
        self._depth = depth

    def make_move(self, game: ConnectFourGame, previous_move: Optional[int]) -> int:
        """Make a move in the given Connect Four game as described in the docstring for this class.
        Return the move that was made.

        <previous_move> is the opponent's' most recent move, or None if no moves have been made.

        If the depth of this player <= 3, add a slight delay (0.5 seconds) before the AI makes
        a move.

        Preconditions:
            - There is at least one valid move for the given game
        """

        if self._depth <= 3:
            time.sleep(0.5)

        player = 'Red' if game.is_red_move() else 'Yellow'
        if previous_move is None:
            tree = game_tree.GameTree(player, game_tree.ROOT_MOVE, game)
            move = tree.minimax(self._depth)
        else:
            tree = game_tree.GameTree(player, previous_move, game)
            move = tree.minimax(self._depth)

        game.make_move(move)
        return move


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'connect_four', 'game_tree', 'random', 'time'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import doctest
    doctest.testmod(verbose=True)
