"""CSC111 Winter 2021 Final Project: Connect Four Game Basics

Module Description
===============================
This Python module contains the class that is used to represent games of Connect Four. This class
contains a collection of methods that govern a game of connect four (i.e, dropping pieces into
the board, detecting when a game is over, etc.)

Copyright Information
===============================
This file is Copyright (c) 2021 Anis Singh.
"""
from __future__ import annotations
from typing import Optional
import copy
import numpy as np

# Global Constants
EMPTY_PIECE = 0
RED_PIECE = 1
YELLOW_PIECE = 2

_ROWS = 6
_COLS = 7


class ConnectFourGame:
    """A class representing a state of a game of Connect Four.

    >>> game = ConnectFourGame()
    >>> game.is_red_move()
    True
    >>> game.get_valid_moves()
    [0, 1, 2, 3, 4, 5, 6]
    >>> game.make_move(3)
    >>> game.is_red_move()
    False
    >>> game.make_move(3)
    >>> game.get_board()
    array([[0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 2., 0., 0., 0.],
           [0., 0., 0., 1., 0., 0., 0.]])
    >>> game.get_winner() is None
    True
    """
    # Private Instance Attributes:
    #   - _board: a two-dimensional array representing a Connect Four board
    #   - _valid_moves: a list of the valid moves for the current player
    #   - _rows: the number of rows of this board
    #   - _cols: the number of columns of this board
    #   - _red_move: a boolean representing whether red is the current player
    #   - _moves_made: the total amount of moves that have been made in this game
    #   - _max_moves: the maximum possible number of moves that can be made before this game
    #                 must be over
    _board: np.ndarray
    _valid_moves: list[int]
    _red_move: bool
    _rows: int
    _cols: int
    _moves_made: int
    _max_moves: int

    def __init__(self, red_move: bool = True) -> None:
        """Initialize a new Connect Four Game with a board that has 6 rows and 7 columns.
        Whether or not red is first to move is determined by <red_move>.
        """
        # Note: I was originally planning on making it so connect four boards can have
        # a customizable amount of rows and columns. This ended up adding too much
        # complexity to my code, and I decided to discontinue it, but this is a feature I
        # want to add to this program over the summer, so I did not want to re-configure my
        # code to remove the potential to implement this. After speaking to David in office hours,
        # he told me I should leave a comment in here explaining that this is why I'm using private
        # instance attributes for the rows and columns of the board, rather than just using the
        # constants defined at the top of the file.
        self._rows = _ROWS
        self._cols = _COLS
        self._board = np.zeros((self._rows, self._cols))
        self._valid_moves = list(range(self._cols))
        self._red_move = red_move
        self._moves_made = 0
        self._max_moves = self._rows * self._cols

    def make_move(self, col: int) -> None:
        """Place a piece in the appropriate row for the column <col>.

        Raise a ValueError if the given move is invalid.

        Preconditions:
            - 0 <= col <= self.get_cols() - 1
        """
        # Check if move is valid
        if self.is_valid_move(col):
            # Get the appropriate row
            row = self._get_row_for_move(col)

            # Mutate the game board
            self._board[row][col] = RED_PIECE if self._red_move else YELLOW_PIECE
        else:
            raise ValueError(f'Cannot place a piece in column "{col}"')

        # Change active player
        self._red_move = not self._red_move

        # Update moves made in this game
        self._moves_made += 1

        # Update the valid moves for the game state
        self._calculate_valid_moves()

    def is_valid_move(self, col: int) -> bool:
        """Check if a piece can be placed into the column <col> on the board.

        Preconditions:
            - 0 <= col <= self.get_cols() - 1
        """
        # A move is valid iff the top row of the column that the piece will be placed in
        # is not filled.

        # Want to return a bool instead of a numpy.bool_ object
        return bool(self._board[self._rows - 1][col] == 0)

    def get_valid_moves(self) -> list[int]:
        """Return a list of the valid columns for a player to drop a piece into."""
        return self._valid_moves

    def get_winner(self) -> Optional[str]:
        """Return the winner of this game ('Red' or 'Yellow'). If the game ended in
        a draw, then 'Draw' is returned.

        If the game is not over yet, return None.

        Preconditions:
            - the game was not previously over (i.e. only the most recent move could possibly
              cause the game to have ended).
        """
        if self._moves_made >= self._max_moves:
            return 'Draw'
        elif self._is_winner():
            return 'Yellow' if self._red_move else 'Red'
        else:
            return None

    def copy_and_make_move(self, move: int) -> ConnectFourGame:
        """Make the given move in a copy of this ConnectFourGame, and return that copy.

        If move is not a valid move, raise a ValueError.
        """
        if self.is_valid_move(move):
            new_board = copy.deepcopy(self._board)
            row = self._get_row_for_move(move)

            # Mutate the new game board
            new_board[row][move] = RED_PIECE if self._red_move else YELLOW_PIECE
            # Create the new game instance
            new_game = ConnectFourGame(red_move=not self._red_move)
            # Update instance attributes
            new_game._board, new_game._moves_made = new_board, self._moves_made + 1
            new_game._calculate_valid_moves()
            return new_game
        else:
            raise ValueError(f'Cannot place a piece in column "{move}"')

    def get_cols(self) -> int:
        """Return the number of columns of the board."""
        return self._cols

    def get_rows(self) -> int:
        """Return the number of rows of the board."""
        return self._rows

    def get_board(self) -> np.ndarray:
        """Return an array representation of the current state of the game board."""
        return np.flip(self._board, 0)

    def is_red_move(self) -> bool:
        """Return whether it is red's move or not."""
        return self._red_move

    def _get_row_for_move(self, col: int) -> int:
        """Return the row that a piece should be placed on when dropped into the column <col>.

        Preconditions:
            - self.is_valid_move(col)
        """
        # Find the first row with a 0 (no piece) and return it
        for row in range(0, self._rows):
            if self._board[row][col] == 0:
                return row
        # The move is valid, so we cannot reach this line of code
        assert False

    def _is_winner(self) -> bool:
        """Return whether or not the previous move made was a winning move."""
        # Check the move made by the previous player
        piece = RED_PIECE if not self._red_move else YELLOW_PIECE

        # Check for horizontal four in a rows
        for col in range(0, self._cols - 3):
            for row in range(0, self._rows):
                # Check if we have a four in a row
                if all(self._board[row][col + i] == piece for i in range(0, 4)):
                    return True

        # Check for vertical four in a rows
        for col in range(0, self._cols):
            for row in range(0, self._rows - 3):
                # Check if we have a four in a row
                if all(self._board[row + i][col] == piece for i in range(0, 4)):
                    return True

        # Check for diagonal four in rows that look like: "/"
        for col in range(0, self._cols - 3):
            for row in range(0, self._rows - 3):
                # Check if we have a four in a row
                if all(self._board[row + i][col + i] == piece for i in range(0, 4)):
                    return True

        # Check for diagonal four in a rows that look like: "\"
        for col in range(0, self._cols - 3):
            for row in range(3, self._rows):
                # Check if we have a four in a row
                if all(self._board[row - i][col + i] == piece for i in range(0, 4)):
                    return True

        # If we have not yet returned a value, the previous move was not a winning move
        return False

    def _calculate_valid_moves(self) -> None:
        """Update self._valid_moves so that it contains the valid moves of current state of
        the game."""
        valid_moves = []
        for col in range(0, self._cols):
            if self.is_valid_move(col):
                valid_moves.append(col)
        self._valid_moves = valid_moves


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'numpy', 'pygame', 'copy'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136', 'R1710']
    })

    import doctest
    doctest.testmod(verbose=True)
