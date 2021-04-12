"""This is the file that uses Tkinter to create a visualization of the game.
will be implemented after the algorithms for the game is done. """
import tkinter as tk
from Player import IntelligentPlayer
from ChessGame import ChessGame
from typing import Optional
import math

ai_turn = False
game = ChessGame()


def take_move(event) -> None:
    """Let the user take their move and draw the piece on the game board"""
    global game_state, white_number
    x = event.x
    y = event.y
    print(x, y)
    move = area_recognition(x, y)

    if game.get_board()[move[0]][move[1]] is not None or move is None:
        return None
    else:
        # breakpoint()
        draw_cord = get_coordinate(move)
        draw_piece((draw_cord[0], draw_cord[1]), 'white')
        game.make_move(move)
        white_number += 1
        if game.get_score() == -1 * math.inf:
            val_state.set("You won!")
            return None
        val_state.set("AI is currently thinking!")


def ai_move(event) -> None:
    """Let the ai take its move and draw the piece on the board"""
    global black_number
    if val_state.get() == 'You won!' or white_number != black_number:
        return None
    ai_next_move = ai.choose_move()
    draw_cord = get_coordinate(ai_next_move)
    game.make_move(ai_next_move)
    print(f"AI: {ai_move}")
    draw_piece((draw_cord[0], draw_cord[1]), 'black')
    black_number += 1
    val_state.set("It's your turn!")
    if game.get_score() == math.inf:
        val_state.set("You lost!")


def area_recognition(x, y) -> Optional[tuple[int, int]]:
    """Return the coordinate of the move on the board.
    """
    if x < 20 or x > 660 or y < 20 or y > 660:
        return None

    hor = (x // 40) - 1
    h_remainder = x % 40
    ver = (y // 40) - 1
    v_remainder = y % 40

    if h_remainder > 20:
        hor += 1
    if v_remainder > 20:
        ver += 1

    assert 0 <= hor < 15 and 0 <= ver < 15
    print(hor, ver)
    return (hor, ver)


def get_coordinate(cord: tuple[int, int]) -> tuple[int, int]:
    """Return the coordinate of this piece on the canvas"""
    x = (cord[0] + 1) * 40
    y = (cord[1] + 1) * 40
    return (x, y)


def draw_piece(cord: tuple[int, int], kind: str) -> None:
    """Draw the piece on the canvas.
    """
    radius = 10
    if kind == 'white':
        kind = 'silver'
    canvas.create_oval(cord[0] - radius, cord[1] - radius,
                       cord[0] + radius, cord[1] + radius, fill=kind)


def _draw_chess_board() -> None:
    """Draw a new chess board.
    """
    for i in range(15):
        start = (40, (i + 1) * 40)
        end = (600, (i + 1) * 40)
        canvas.create_line(start[0], start[1], end[0], end[1])

        start = ((i + 1) * 40, 40)
        end = ((i + 1) * 40, 600)
        canvas.create_line(start[0], start[1], end[0], end[1])
        for j in range(15):
            coordinate = ((i + 1) * 40, (j + 1) * 40)
            canvas.create_oval(coordinate[0] - 2, coordinate[1] - 2,
                               coordinate[0] + 2, coordinate[1] + 2, fill='black')

    # Draw the first black piece.
    cor = get_coordinate((7, 7))
    draw_piece(cor, 'black')


def restart() -> None:
    """Restart the game.
    """
    global ai_turn, game, black_number, white_number
    ai_turn = False
    game.restart()
    game.make_move((7, 7))
    canvas.delete('all')
    _draw_chess_board()
    val_state.set("The game is ongoing")
    white_number, black_number = 0, 1


def change_mode(depth: int) -> None:
    """..."""
    global ai
    ai.depth = depth


def auxiliary_widgets() -> None:
    """Add auxiliary widgets.
    """
    global game_state, start_button, val_state
    val_state = tk.StringVar()
    val_state.set("The game is ongoing")
    game_state = tk.Label(window, textvariable=val_state, font=('Arial', 20), width=30,
                          height=2)
    game_state.place(x=800, y=150, anchor='nw')

    start_button = tk.Button(window, text="Restart", width=15, height=2, command=restart)
    start_button.place(x=900, y=500, anchor='nw')

    # b_1 = tk.Button(window, text="Easy Mode", width=30, height=2, command=change_mode(2))
    # b_1.place(x=850, y=250)

    # b_2 = tk.Button(window, text="Hard Mode(Longer running Time)", width=30, height=2,
    #                 command=change_mode(4))
    # b_2.place(x=850, y=350)


if __name__ == '__main__':
    """Visualize the chess game.
        """
    white_number = 0
    black_number = 0

    window = tk.Tk()
    window.title('Five in A Row Game')
    window.geometry('1200x800')

    # Canvas.
    canvas = tk.Canvas(window, height=750, width=750, bg='white')
    canvas.place(x=0, y=0, anchor='nw')

    # Draw Chess board.
    _draw_chess_board()

    # Create an AI player.
    game = ChessGame()
    game.make_move((7, 7))
    black_number += 1
    ai = IntelligentPlayer('black', game)

    # Auxiliary Button.
    auxiliary_widgets()

    canvas.bind('<Button-1>', take_move)
    canvas.bind('<ButtonRelease-1>', ai_move)

    window.mainloop()
