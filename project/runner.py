"""CSC111 Winter 2021 Final Project: Running Connect Four Games Module

Module Description
===============================
This Python module contains the functions responsible for running games of Connect Four between a
user and an AI of a certain skill level, between two AIs, or between two users.

Copyright Information
===============================
This file is Copyright (c) 2021 Anis Singh.
"""
import pygame
import plotly.graph_objects as go
import visualizer as v
import players as p
from connect_four import ConnectFourGame


def run_game(d: int = 5, red_starts: bool = True) -> None:
    """Run a Connect Four Game between a user and a Minimax AI. The user player is always red and
    the AI player is always yellow.

    The depth that the AI uses the minimax algorithm to is determined by <d>. Whether or
    not the user starts is determined by <red_starts>.

    Preconditions:
        - d > 0
        - must be on a monitor that is at least 840 x 840

    Note: Calling this function with d >= 6 is not recommended, as the AI begins to take a long
    time to make a move.
    """
    game, screen = _setup_game([pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION], red_starts)
    ai_player = p.MinimaxPlayer(depth=d)
    user_quit = False
    previous_move = None

    # Main game loop
    while game.get_winner() is None:

        v.draw_game_state(game, screen)
        pygame.display.flip()

        # Wait for an event if it is the user's turn
        if game.is_red_move():
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                col_clicked = v.get_mouse_click_col(event, screen.get_size())
                previous_move = p.user_make_move(game, previous_move, col_clicked)

                # Wipe phantom circle from top
                v.clear_top_row(screen)

            elif event.type == pygame.MOUSEMOTION:
                v.draw_phantom_circle(game, event.pos[0], screen)

            elif event.type == pygame.QUIT:
                user_quit = True
                break

        # AI's turn
        else:
            previous_move = ai_player.make_move(game, previous_move)
            # Draw phantom circle for red in the centre so they know the AI has made its move
            v.draw_phantom_circle(game, screen.get_width() // 2, screen)

    v.update_game_end(game, screen, user_quit)


def run_games_ai(n: int, d: int = 5, rand_starts: bool = False) -> None:
    """Run <n> games between an AI that makes random moves and an AI that uses the minimax
    algorithm to depth <d>. Whether or not the Random AI starts or not is determined by
    <rand_starts>. The AI that uses the minimax algorithm is always yellow, and the
    AI that plays randomly is always red.

    Report the results of these games in both a text-based way (printing results to the console)
    and in a visual way.

    Should the user exit the pygame window before all <n> games are played, display only the
    statistics of the games that were fully completed.

    Preconditions:
        - n > 0
        - d > 0
        - must be on a monitor of at least 840 x 840
    """
    minimax_ai = p.MinimaxPlayer(depth=d)  # Yellow player
    opponent = p.RandomPlayer()  # Red player
    minimax_ai_wins, opponent_wins, draws = 0, 0, 0

    # Set up pygame screen
    screen_size = (840, 840)
    allowed_events = []
    screen = v.initialize_screen(screen_size, allowed_events)

    winner = ''

    for i in range(0, n):
        game = ConnectFourGame(red_move=rand_starts)

        winner = _run_ai_game(screen, game, minimax_ai, opponent)

        if winner == 'Yellow':
            print(f'Game {i + 1} Winner: Minimax Depth {d} AI.')
            minimax_ai_wins += 1
        elif winner == 'Red':
            print(f'Game {i + 1} Winner: Random AI.')
            opponent_wins += 1
        elif winner == 'Draw':
            print(f'Game {i + 1} ended in a draw.')
            draws += 1
        else:
            assert winner == 'QUIT'
            break

    print(f'Minimax Depth {d} AI won: {minimax_ai_wins} games.')
    print(f'Random AI won: {opponent_wins} games.')
    print(f'{draws} games ended in a draw.')

    _plot_game_statistics(opponent_wins, minimax_ai_wins, draws, 'Random AI Wins',
                          f'Minimax Depth {d} AI Wins')

    if winner != 'QUIT':
        # Wait for the user to quit
        v.wait_for_quit()


def run_game_two(red_starts: bool = True) -> None:
    """Run a Connect Four Game between two players (no AI). The player that starts this game is
    determined by <red_starts>.

    Preconditions:
        - must be on a monitor that is at least 840 x 840
    """
    game, screen = _setup_game([pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION], red_starts)
    user_quit = False
    previous_move = None

    while game.get_winner() is None:

        v.draw_game_state(game, screen)
        pygame.display.flip()

        # Wait for an event
        event = pygame.event.wait()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            col_clicked = v.get_mouse_click_col(event, screen.get_size())
            previous_move = p.user_make_move(game, previous_move, col_clicked)

            # Draw phantom circle on top
            v.draw_phantom_circle(game, event.pos[0], screen)

        elif event.type == pygame.MOUSEMOTION:
            v.draw_phantom_circle(game, event.pos[0], screen)

        elif event.type == pygame.QUIT:
            user_quit = True
            break

    v.update_game_end(game, screen, user_quit)


def _run_ai_game(screen: pygame.Surface, game: ConnectFourGame, minimax_ai: p.MinimaxPlayer,
                 opponent: p.RandomPlayer) -> str:
    """Run a visual game between a Minimax AI player and a Random AI player and return the winner.
    If the window is closed before the game is over, stop running the game and return 'QUIT'.
    """
    user_quit = False
    previous_move = None
    while game.get_winner() is None:

        if user_quit:
            break

        v.draw_game_state(game, screen)
        pygame.display.flip()

        for _ in pygame.event.get(pygame.QUIT):
            pygame.display.quit()
            pygame.quit()
            user_quit = True

        if game.is_red_move():
            previous_move = opponent.make_move(game, previous_move)
        else:
            previous_move = minimax_ai.make_move(game, previous_move)

    if user_quit:
        return 'QUIT'
    else:
        # Draw the final game state
        v.draw_game_state(game, screen)

        # Draw the winner of the game on the screen and let it stay there for slightly over
        # a second
        v.draw_winner(game, screen)
        pygame.time.wait(1250)

        v.clear_top_row(screen)
        return game.get_winner()


def _plot_game_statistics(red_wins: int, yellow_wins: int, draws: int,
                          red_wins_title: str = 'Red Wins',
                          yellow_wins_title: str = 'Yellow Wins') -> None:
    """Visually display the results of a sequence of Connect Four games."""

    # Create the figure object
    fig = go.Figure(data=[
        go.Bar(name=red_wins_title, x=[red_wins_title], y=[red_wins]),
        go.Bar(name=yellow_wins_title, x=[yellow_wins_title], y=[yellow_wins]),
        go.Bar(name='Draws', x=['Draws'], y=[draws])
    ])

    # Add titles
    fig.update_layout(title='Connect Four Game Results', xaxis_title='Outcome')

    # Display the figure
    fig.show()


def _setup_game(allowed_events: list, red_starts: bool = True) -> (ConnectFourGame, pygame.Surface):
    """Set up and initialize a pygame screen and a generic Connect Four game where
    the starting player is determined by <red_starts>. The only allowed pygame
    events are determined by <allowed_events>.

    Return a tuple containing the Connect Four game and the pygame screen in the form
    (game, screen).
    """
    # Initialize a connect four game
    game = ConnectFourGame(red_move=red_starts)

    # Set the screen size
    screen_size = (v.SIZE_OF_CIRCLES * game.get_cols(), v.SIZE_OF_CIRCLES * (game.get_rows() + 1))

    # Initialize and return a Pygame screen
    screen = v.initialize_screen(screen_size, allowed_events)
    return (game, screen)


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    # Note: Leaving this uncommented results in the AIs taking longer to make moves.
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'visualizer', 'players', 'plotly.graph_objects',
                          'pygame', 'connect_four'],
        'allowed-io': ['run_games_ai'],
        'max-line-length': 100,
        'disable': [],
        'generated-members': ['pygame.*']
    })

    import doctest
    doctest.testmod(verbose=True)
