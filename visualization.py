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
    global game_state
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
        if game.get_score() == -1 * math.inf:
            val_state.set("You won!")
            return None
        val_state.set("AI is currently thinking!")

        # ai_move = ai.choose_move()
        # draw_cord = get_coordinate(ai_move)
        # game.make_move(ai_move)
        # print(f"AI: {ai_move}")
        # draw_piece((draw_cord[0], draw_cord[1]), 'black')
        # if game.get_score() == math.inf:
        #     val_state.set("You lost!")


def ai_move(event) -> None:
    """Let the ai take its move and draw the piece on the board"""
    if val_state.get() == 'You won!':
        return None
    ai_next_move = ai.choose_move()
    draw_cord = get_coordinate(ai_next_move)
    game.make_move(ai_next_move)
    print(f"AI: {ai_move}")
    draw_piece((draw_cord[0], draw_cord[1]), 'black')
    val_state.set("It's your turn!")
    if game.get_score() == math.inf:
        val_state.set("You lost!")


def area_recognition(x, y) -> Optional[tuple[int, int]]:
    """Return the coordinate of the move on the board.
    """
    if x < 25 or x > 775 or y < 25 or y > 775:
        return None

    hor = (x // 50) - 1
    h_remainder = x % 50
    ver = (y // 50) - 1
    v_remainder = y % 50

    if h_remainder > 25:
        hor += 1
    if v_remainder > 25:
        ver += 1

    assert 0 <= hor < 15 and 0 <= ver < 15
    print(hor, ver)
    return (hor, ver)


def get_coordinate(cord: tuple[int, int]) -> tuple[int, int]:
    """Return the coordinate of this piece on the canvas"""
    x = (cord[0] + 1) * 50
    y = (cord[1] + 1) * 50
    return (x, y)


def draw_piece(cord: tuple[int, int], kind: str) -> None:
    """Draw the piece on the canvas.
    """
    radius = 13
    if kind == 'white':
        kind = 'silver'
    canvas.create_oval(cord[0] - radius, cord[1] - radius,
                       cord[0] + radius, cord[1] + radius, fill=kind)


def _draw_chess_board() -> None:
    """Draw a new chess board.
    """
    for i in range(15):
        start = (50, (i + 1) * 50)
        end = (800, (i + 1) * 50)
        canvas.create_line(start[0], start[1], end[0], end[1])

        start = ((i + 1) * 50, 50)
        end = ((i + 1) * 50, 800)
        canvas.create_line(start[0], start[1], end[0], end[1])
        for j in range(15):
            coordinate = ((i + 1) * 50, (j + 1) * 50)
            canvas.create_oval(coordinate[0] - 2, coordinate[1] - 2,
                               coordinate[0] + 2, coordinate[1] + 2, fill='black')

    # Draw the first black piece.
    cor = get_coordinate((7, 7))
    draw_piece(cor, 'black')


def restart() -> None:
    """Restart the game.
    """
    global ai_turn, game
    ai_turn = False
    game.restart()
    game.make_move((7, 7))
    canvas.delete('all')
    _draw_chess_board()
    val_state.set("The game is ongoing")


def change_mode(depth: int) -> None:
    """..."""
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

    # var = tk.StringVar()
    # radio_1 = tk.Radiobutton(window, text='Easy Mode', variable=var, value='A',
    #                          command=change_mode(2))
    # radio_1.place(x=850, y=250)

    # radio_2 = tk.Radiobutton(window, text='Hard Mode(longer time)', variable=var, value='B',
    #                          command=change_mode(3))
    # radio_2.place(x=850, y=350)


if __name__ == '__main__':
    """Visualize the chess game.
        """
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
    ai = IntelligentPlayer('black', game)

    # Auxiliary Button.
    auxiliary_widgets()

    canvas.bind('<Button-1>', take_move)
    canvas.bind('<ButtonRelease-1>', ai_move)

    window.mainloop()
