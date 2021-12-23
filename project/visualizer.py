"""CSC111 Winter 2021 Final Project: Connect Four Game Visualizer

Module Description
===============================
This Python module contains the functions responsible for visualizing Connect Four games
in an interactive way.

Copyright Information
===============================
This file is Copyright (c) 2021 Anis Singh.
"""
import pygame
from pygame.colordict import THECOLORS
from connect_four import ConnectFourGame, EMPTY_PIECE, RED_PIECE, YELLOW_PIECE

# Global constants
SIZE_OF_CIRCLES = 120
RADIUS_OFFSET = 7
RADIUS_OF_CIRCLES = SIZE_OF_CIRCLES // 2 - RADIUS_OFFSET


def initialize_screen(screen_size: tuple[int, int], allowed_events: list) -> pygame.Surface:
    """Initialize pygame and the display window.

    This function is similar to a function from Assignment 1. The handout for this assignment
    can be found here: https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/a1/handout/
    """
    pygame.display.init()
    pygame.font.init()

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Connect Four')
    screen.fill(THECOLORS['white'])
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed_events)

    return screen


def draw_text(screen: pygame.Surface, text: str, pos: tuple[int, int], font_size: int,
              colour: str) -> None:
    """Draw <text> with the given font size and colour onto the given pygame screen at
    <pos>.

    <pos> refers to the upper-left corner of where the text will be drawn.

    This function is a modified version of a function from Assignment 1. The handout for this
    assignment can be found here:
    https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/a1/handout/

    Preconditions:
        - colour in THECOLORS
    """
    font = pygame.font.SysFont('arial', font_size)
    text_surface = font.render(text, True, THECOLORS[colour])
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def draw_game_state(game: ConnectFourGame, screen: pygame.Surface) -> None:
    """Draw the game state of <game> on <screen>.

    Preconditions:
        - screen.get_width() >= 840
        - screen.get_height() >= 840
    """
    rect_offset = SIZE_OF_CIRCLES
    circ_offset = SIZE_OF_CIRCLES // 2
    for col in range(0, game.get_cols()):
        for row in range(0, game.get_rows()):
            rect = pygame.Rect(col * SIZE_OF_CIRCLES, row * SIZE_OF_CIRCLES + rect_offset,
                               SIZE_OF_CIRCLES, SIZE_OF_CIRCLES)
            circle_pos = (col * SIZE_OF_CIRCLES + circ_offset,
                          row * SIZE_OF_CIRCLES + rect_offset + circ_offset)

            pygame.draw.rect(screen, THECOLORS['blue'], rect)
            _draw_circle(screen, game, row, col, circle_pos)


def draw_phantom_circle(game: ConnectFourGame, x_pos: int, screen: pygame.Surface) -> None:
    """Draw a 'phantom' circle centred at <x_pos> in the top row of <screen>.

    Preconditions:
        - 0 <= x_pos <= screen.get_width()
        - screen.get_width() >= 840
        - screen.get_height() >= 840
    """
    # Wipe any potential phantom circles that were already there
    clear_top_row(screen)

    # Draw the "phantom" circle
    circ_centre = (x_pos, SIZE_OF_CIRCLES // 2)
    if game.is_red_move():
        pygame.draw.circle(screen, THECOLORS['red'], circ_centre, RADIUS_OF_CIRCLES)
    else:
        pygame.draw.circle(screen, THECOLORS['yellow'], circ_centre, RADIUS_OF_CIRCLES)


def clear_top_row(screen: pygame.Surface) -> None:
    """Clear the top row of <screen> by drawing a white rectangle over it. The drawn rectangle
    has width screen.get_width(), and height 120.

    Preconditions:
        - screen.get_width() >= 840
        - screen.get_height() >= 840
    """
    pygame.draw.rect(screen, THECOLORS['white'], (0, 0, screen.get_width(), SIZE_OF_CIRCLES))


def get_mouse_click_col(event: pygame.event.Event, screen_size: tuple[int, int]) -> int:
    """Return the column that was left-clicked on by a user.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - event.button == 1
        - screen.get_width() >= 840
        - screen.get_height() >= 840
    """
    width = screen_size[0]
    cell_width = SIZE_OF_CIRCLES

    curr_x_pos = 0
    curr_col = 0
    event_x_pos = event.pos[0]

    while curr_x_pos <= width:
        if curr_x_pos <= event_x_pos <= curr_x_pos + cell_width:
            return curr_col
        curr_x_pos = curr_x_pos + cell_width
        curr_col += 1


def update_game_end(game: ConnectFourGame, screen: pygame.Surface, user_quit: bool) -> None:
    """Update the screen when the Connect Four game ends. The game can end due to the
    user quitting or the game being over. If it ended because the game was over, display
    the outcome of the game on the top of the screen and wait for the user to quit.

    Preconditions:
        - screen.get_width() >= 840
        - screen.get_height() >= 840
    """
    if user_quit:
        pygame.display.quit()
        pygame.quit()
    else:
        # Draw the final game state
        draw_game_state(game, screen)

        # Wipe phantom circle from top
        clear_top_row(screen)

        # Draw the winner of the game on the top row
        draw_winner(game, screen)

        # Wait for the user to quit
        wait_for_quit()


def draw_winner(game: ConnectFourGame, screen: pygame.Surface) -> None:
    """Draw the winner of the given Connect Four Game onto the top row of <screen>.

    Preconditions:
        - game.get_winner() is not None
        - screen.get_width() >= 840
        - screen.get_height() >= 840
    """
    winner = game.get_winner()

    if winner == 'Draw':
        draw_text(screen, winner + '!', (2 * screen.get_width() // 5, 10), 75, 'black')
    else:
        draw_text(screen, winner + ' wins!', (5 * screen.get_width() // 16, 10), 75, winner.lower())
    pygame.display.flip()


def wait_for_quit() -> None:
    """Wait until the user closes the pygame window.

    This function is borrowed from Tutorial 9. A link to the tutorial handout can be found here:
    https://www.teach.cs.toronto.edu/~csc111h/winter/tutorials/09-iterative-sorting/

    Preconditions:
        - pygame window has been opened
    """
    while True:
        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            break
    pygame.display.quit()
    pygame.quit()


def _draw_circle(screen: pygame.Surface, game: ConnectFourGame, row: int, col: int,
                 circle_pos: tuple[int, int]) -> None:
    """Draw the circle that is colour coded corresponding to the player whose piece is
    placed at game.get_board()[row][col].

    Preconditions:
        - 0 <= row <= game.get_rows() - 1
        - 0 <= col <= game.get_cols() - 1
        - screen.get_width() >= 840
        - screen.get_height() >= 840
    """
    if game.get_board()[row][col] == EMPTY_PIECE:
        pygame.draw.circle(screen, THECOLORS['white'], circle_pos, RADIUS_OF_CIRCLES)
    elif game.get_board()[row][col] == RED_PIECE:
        pygame.draw.circle(screen, THECOLORS['red'], circle_pos, RADIUS_OF_CIRCLES)
    else:
        assert game.get_board()[row][col] == YELLOW_PIECE
        pygame.draw.circle(screen, THECOLORS['yellow'], circle_pos, RADIUS_OF_CIRCLES)


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'pygame', 'pygame.colordict', 'connect_four'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': [],
        'generated-members': ['pygame.*']
    })

    import doctest
    doctest.testmod(verbose=True)
