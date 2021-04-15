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
    global game_state, white_number, val_state
    x = event.x
    y = event.y
    print(x, y)
    move = area_recognition(x, y)

    if game.get_board()[move[0]][move[1]] is not None or move is None or \
            val_state.get() in {"You won!", "You lost!"}:
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
        if white_number == 112:
            val_state.set("Draw")


def ai_move(event) -> None:
    """Let the ai take its move and draw the piece on the board"""
    global black_number, ai
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


def auxiliary_widgets() -> None:
    """Add auxiliary widgets.
    """
    global game_state, start_button, val_state

    # frame = tk.Frame(window)
    # frame.place(x=700, y=500)

    val_state = tk.StringVar()
    val_state.set("The game is ongoing")
    game_state = tk.Label(window, textvariable=val_state, font=('Arial', 20), width=30,
                          height=2)
    game_state.place(x=700, y=350, anchor='nw')

    start_button = tk.Button(window, text="Restart", width=15, height=2, command=restart)
    start_button.place(x=800, y=500, anchor='nw')

    decorations = tk.Canvas(window, height=150, width=250, bg='white')
    decorations.place(x=750, y=100, anchor='nw')
    decorations.create_oval(5, 15, 120, 135,  fill='silver')
    decorations.create_oval(85, 15, 205, 135, fill='black')

    name = tk.Label(window, text="Five in a row", font=('Helvetica', 40), width=15, heigh=1)
    name.place(x=670, y=50)


def init() -> None:
    """Initialize the screen.
    """
    global white_number, black_number, window, canvas, game, ai
    white_number = 0
    black_number = 0

    # window = tk.Tk()
    # window.title('Five in A Row Game')
    # window.geometry('1200x800')

    # Canvas.
    canvas = tk.Canvas(window, height=750, width=1200, bg='white')
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


def clear() -> None:
    """clear the window for the start of the game.
    """
    tutorial.destroy()
    button.destroy()
    init()


if __name__ == '__main__':
    """Visualize the chess game.
        """
    window = tk.Tk()
    window.title('Five in A Row Game')
    window.geometry('1200x800')

    text = "Rules:\n" \
           "Two players, black and white, play on a board of size 15 by 15. Players place \n" \
           "their piece on the board in turn, black taking the first move, and the first \n" \
           "piece must be placed on the center of the board. The goal for each player is \n " \
           "to link their pieces in a row of 5 and/or to stop the other player from doing \n" \
           "so. The player who first links their pieces in a row of 5 wins. The row of five \n"\
           "could be horizontal, vertical, or diagonal. The game ends in a draw when there's \n "\
           " no space for another piece to be placed."
    tutorial = tk.Label(window, text=text, font=('Arial', 25), width=70, height=12)
    tutorial.pack()
    button = tk.Button(window, text="I see", font=("Italic", 40), width=10, height=2, command=clear)
    button.pack()

    window.mainloop()
