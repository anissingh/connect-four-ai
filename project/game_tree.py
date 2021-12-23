"""CSC111 Winter 2021 Final Project: Connect Four GameTree Module

Module Description
===============================
This Python module contains the GameTree class that has a collection of methods that allow it
to use the minimax algorithm to determine the best move for a player to make in a given
scenario.

Copyright Information
===============================
This file is Copyright (c) 2021 Anis Singh.
"""
from __future__ import annotations
import math
from typing import Union, Optional
from connect_four import ConnectFourGame, EMPTY_PIECE, RED_PIECE, YELLOW_PIECE

# Global constants
ROOT_MOVE = 255

FOUR_IN_A_ROW_SCORE = 10000000000
THREE_IN_A_ROW_SCORE = 5
TWO_IN_A_ROW_SCORE = 2
CENTRE_PIECE_WORTH = 3

OPPONENT_FOUR_IN_A_ROW_SCORE = -10000000000
OPPONENT_THREE_IN_A_ROW_SCORE = -4


class GameTree:
    """A decision tree for ConnectFourGame moves from the perspective of one player.

    Each node in the tree stores a ConnectFourGame game state, the move that caused that
    game state to occur, and a boolean value representing the player who's perspective this
    GameTree is in.

    Instance Attributes:
        - game_state: the current state of the Connect Four game.
        - move: the current move, expressed as the column that the piece was dropped in.
        - player: a string representing the player that this GameTree is in the perspective of.

    Representation Invariants:
        - self.player in {'Yellow', 'Red'}
        - self.move == ROOT_MOVE or 0 <= self.move <= self.game_state.get_cols() - 1

    This class is inspired by the GameTree class from Assignment 2. The handout to this assignment
    can be found here: https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/a2/handout/
    """
    game_state: ConnectFourGame
    move: int
    player: str

    # Private Instance Attributes:
    #  -_subtrees: The subtrees of this tree, which represent the game trees after a possible
    #              move by the current player
    #  -_score: Represents the score of this game state (how favourable this game state is)
    #           relative to the player; is either None if the score has not been evaluated,
    #           or an integer if the score has been evaluated. Initialized to None until
    #           it gets calculated. Can be a float as well because, in the minimax algorithm,
    #           it gets assigned to math.inf or -math.inf, which is a float.
    _subtrees: list[GameTree]
    _score: Optional[Union[int, float]]

    def __init__(self, player: str, move: int = ROOT_MOVE,
                 game_state: ConnectFourGame = ConnectFourGame()) -> None:
        """Initialize a new Connect Four Game Tree."""
        self.game_state = game_state
        self.player = player
        self.move = move
        self._score = None
        self._subtrees = []

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)

    def is_terminal_node(self) -> bool:
        """Return whether this node must be a terminal node *relative to self.game_state*.
        """
        # Implementation Note: Cannot just check if self._subtrees is empty! This tree is not
        # necessarily a subtree of another tree that explored every possible valid move from a
        # certain game state yet (this is highly unlikely!)
        return self.game_state.get_winner() is not None

    def minimax(self, d: int) -> int:
        """Apply the minimax algorithm with alpha beta pruning to self up until depth <d> to
        determine the appropriate move to choose. Mutates self by extending this game tree to
        depth <= <d> by adding future game states. Returns the move that should be chosen.

        Preconditions:
            - d > 0
            - the player calling this method is the player who's turn it is in the game
            - this method has not previously been called on self
            - there is at least one valid move in self.game_state

        >>> game = ConnectFourGame()
        >>> game.is_red_move()
        True
        >>> tree = GameTree(player='Red', move=ROOT_MOVE, game_state=game)
        >>> # Find the best starting move for red based on applying the minimax algorithm up to
        >>> # depth 2
        >>> tree.minimax(d=2)
        3
        """
        self._minimax(d, -math.inf, math.inf, True)
        # Note: The below line is why we have the precondition d > 0. If d = 0, this line would
        # return None, and a player cannot play the move None.
        return self._find_move_by_score()

    def _minimax(self, d: int, alpha: Union[float, int], beta: Union[float, int],
                 maximizing_player: bool) -> None:
        """Apply the minimax algorithm with alpha beta pruning to self up until depth <d>.
        Mutates self as described in the minimax docstring.

        Preconditions:
            - d >= 0
        """
        # Terminating Condition (base case)
        if d == 0 or self.is_terminal_node():
            # Score is the heuristic value of the game state
            self._score = self._calculate_score()
            return

        assert self.game_state.get_valid_moves() != []

        if maximizing_player:
            self._minimax_maximizer(d, alpha, beta)

        # Minimizing player
        else:
            self._minimax_minimizer(d, alpha, beta)

    def _minimax_maximizer(self, d: int, alpha: Union[float, int], beta: Union[float, int]) -> None:
        """Helper method to the _minimax method. Performs the minimax algorithm when the
        current player is the maximizing player.
        """
        self._score = -math.inf
        possible_moves = self.game_state.get_valid_moves()
        for move in possible_moves:

            # Create new subtree
            copy_game_state = self.game_state.copy_and_make_move(move)
            subtree = GameTree(self.player, move, copy_game_state)
            self.add_subtree(subtree)

            # Calculate subtree score
            subtree._minimax(d - 1, alpha, beta, False)

            # Update score of self if necessary
            if subtree._score > self._score:
                self._score = subtree._score

            # Alpha-beta pruning
            alpha = max(alpha, self._score)
            if alpha >= beta:
                break
        return

    def _minimax_minimizer(self, d: int, alpha: Union[float, int], beta: Union[float, int]) -> None:
        """Helper method to the _minimax method. Performs the minimax algorithm when the
        current player is the minimizing player.
        """
        self._score = math.inf
        possible_moves = self.game_state.get_valid_moves()
        for move in possible_moves:

            # Create new subtree
            copy_game_state = self.game_state.copy_and_make_move(move)
            subtree = GameTree(self.player, move, copy_game_state)
            self.add_subtree(subtree)

            # Calculate subtree score
            subtree._minimax(d - 1, alpha, beta, True)

            # Update score of self if necessary
            if subtree._score < self._score:
                self._score = subtree._score

            # Alpha-beta pruning
            beta = min(beta, self._score)
            if alpha >= beta:
                break
        return

    def _calculate_score(self) -> int:
        """Calculate the score of the *current* board position in the root node of self by
        determining potential power positions (e.g., three in a rows, four in a rows).
        >>> game = ConnectFourGame(red_move=False)
        >>> game.make_move(6)
        >>> game.make_move(6)
        >>> game.make_move(5)
        >>> game.make_move(6)
        >>> game.make_move(3)
        >>> game.make_move(6)
        >>> game.get_board()
        array([[0., 0., 0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0., 0., 1.],
               [0., 0., 0., 0., 0., 0., 1.],
               [0., 0., 0., 0., 0., 0., 1.],
               [0., 0., 0., 2., 0., 2., 2.]])
        >>> # Create a game tree from red's perspective and calculate its score
        >>> tree_red = GameTree(player='Red', move=6, game_state=game)
        >>> tree_red._calculate_score()
        3
        >>> # Create a game tree from yellow's perspective and calculate its score
        >>> tree_yellow = GameTree(player='Yellow', move=6, game_state=game)
        >>> tree_yellow._calculate_score()
        6
        """
        # Note: Notice that this method considers ALL possible combinations of four, three,
        # and two in a rows! For example, the following sequence: 1, 1, 1, 1, 0, 0, ... is an
        # example of a four in a row for red, but also a three in a row, and a two in a row! Each
        # of these will have separate influences on a player's evaluation of the board. Also, some
        # diagonals can be counted twice (they will be detected as both a forward and a backward
        # diagonal. See the note in the helper function _score_sub_section to better understand why
        # this is.
        score = 0
        game, player = self.game_state, self.player

        # Assign a score of 0 to boards that end in a draw
        if game.get_winner() == 'Draw':
            return score

        # Check the board from the perspective of the player
        piece = RED_PIECE if player == 'Red' else YELLOW_PIECE

        rows, cols = game.get_rows(), game.get_cols()

        # Check centre of board first (more opportunities can be created from centre pieces)
        sub_centre = [int(board_piece) for board_piece in list(game.get_board()[:, cols // 2])]
        score += CENTRE_PIECE_WORTH * sub_centre.count(piece)

        # Check rows
        for row in range(0, rows):
            curr_row = [int(board_piece) for board_piece in list(game.get_board()[row, :])]
            # Don't start with last three columns
            for col in range(0, cols - 3):
                # Check four pieces at a time
                sub_row = curr_row[col:col + 4]
                score += _score_sub_section(sub_row, piece)

        # Check columns in a similar manner
        for col in range(0, cols):
            curr_col = [int(board_piece) for board_piece in list(game.get_board()[:, col])]
            for row in range(0, rows - 3):
                sub_col = curr_col[row:row + 4]
                score += _score_sub_section(sub_col, piece)

        # Check "/" diagonals
        for row in range(0, rows - 3):
            for col in range(0, cols - 3):
                # Row increases, column increases
                diagonal = [int(game.get_board()[row + i][col + i]) for i in range(0, 4)]
                score += _score_sub_section(diagonal, piece)

        # Check "\" diagonals
        for row in range(0, rows - 3):
            for col in range(0, cols - 3):
                # Row decreases, column increases
                diagonal = [int(game.get_board()[row + 3 - i][col + i]) for i in range(0, 4)]
                score += _score_sub_section(diagonal, piece)

        return score

    def _find_move_by_score(self) -> Optional[int]:
        """Return the move that should be made based on the score of this GameTree. This method
        should only be called immediately after the minimax algorithm was applied to self.

        Return None if there is no appropriate move.
        """
        for subtree in self._subtrees:
            if subtree._score == self._score:
                return subtree.move

        return None


def _score_sub_section(section: list[int], piece: int) -> int:
    """Score the sub-section <section> of the board from the perspective of the player that plays
    with <piece> and return this score."""
    score = 0
    opponent_piece = RED_PIECE if piece == YELLOW_PIECE else YELLOW_PIECE

    # Note: Three in a rows and two in a rows are weighted MUCH less than four in a rows because:
    #   1. Four in a rows with empty columns beside them can also produce subsequent three AND
    #      two in a rows when different sections of the board are passed to this function (i.e.,
    #      a section only containing 3 of the pieces of the four in a row and also an empty spot
    #      will be detected by this algorithm as a three in a row as well). This is intentional!
    #      It allows the player to detect 'forks' (positions that, no matter what piece a player
    #      plays, the other player receives an advantage either way; a 'forcing move' in a sense).
    #   2. When playing at a certain depth, most base cases in the minimax algorithm will find
    #      four in a rows, so three and two in a rows become more irrelevant.

    # Four in a row
    if section.count(piece) == 4:
        score += FOUR_IN_A_ROW_SCORE
    # Three in a row
    elif section.count(piece) == 3 and section.count(EMPTY_PIECE) == 1:
        score += THREE_IN_A_ROW_SCORE
    # Two in a row
    elif section.count(piece) == 2 and section.count(EMPTY_PIECE) == 2:
        score += TWO_IN_A_ROW_SCORE

    # Opponent four in a row
    if section.count(opponent_piece) == 4:
        score += OPPONENT_FOUR_IN_A_ROW_SCORE
    # Opponent three in a row
    elif section.count(opponent_piece) == 3 and section.count(EMPTY_PIECE) == 1:
        score += OPPONENT_THREE_IN_A_ROW_SCORE
    # Note: After extensive testing, opponent two in a rows were removed, as they
    # did not contribute much (their heuristic value was -1, which is almost
    # nothing).

    return score


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    # Note: Leaving this call uncommented makes the minimax algorithm significantly slower.
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'math', 'connect_four'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import doctest
    doctest.testmod(verbose=True)
