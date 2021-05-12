"""This is the file that uses Tkinter to create a visualization of the game.
will be implemented after the algorithms for the game is done. """
import tkinter as tk
from Player import IntelligentPlayer
from ChessGame import ChessGame
from typing import Optional
import math
from PIL import Image, ImageTk

# The depth of AI, change this variable only if you got a great discrete graphics or sufficient time
# waiting for processing.
# DEPTH = 2


def take_move(event) -> None:
    """Let the user take their move and draw the piece on the game board"""
    global game_state, white_number, val_state
    x = event.x
    y = event.y
    print(x, y)
    move = area_recognition(x, y)

    if move is None or game.get_board()[move[0]][move[1]] is not None or \
            val_state.get() in {"You won!", "You lost!"}:
        return None
    else:

        p_label.configure(image=p_2)
        p_label.image = p_2

        # breakpoint()
        draw_cord = get_coordinate(move)
        draw_piece((draw_cord[0], draw_cord[1]), 'white')
        game.make_move(move)
        white_number += 1
        if game.get_score() == -1 * math.inf:
            val_state.set("You won!")
            p_label.configure(image=p_3)
            p_label.image = p_3
            return None
        val_state.set("AI is currently thinking!")
        if white_number == 112:
            val_state.set("Draw")


def ai_move(event) -> None:
    """Let the ai take its move and draw the piece on the board"""
    global black_number, ai, p_2, p_label
    if val_state.get() == 'You won!' or white_number != black_number:
        return None

    p_label.configure(image=p_1)
    p_label.image = p_1

    ai_next_move = ai.choose_move()
    draw_cord = get_coordinate(ai_next_move)
    game.make_move(ai_next_move)
    print(f"AI: {ai_move}")
    draw_piece((draw_cord[0], draw_cord[1]), 'black')
    black_number += 1

    val_state.set("It's your turn!")
    if game.get_score() == math.inf:
        val_state.set("You lost!")
        p_label.configure(image=p_4)
        p_label.image = p_4


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
    global canvas
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
    global ai_turn, game, black_number, white_number, p_label
    ai_turn = False
    game.restart()
    game.make_move((7, 7))
    canvas.delete('all')
    _draw_chess_board()
    val_state.set("The game is ongoing")
    white_number, black_number = 0, 1

    p_label.configure(image=p_1)
    p_label.image = p_1


def change_mode(depth: int) -> None:
    """Change the game difficult(not used).
    """
    global ai
    ai.depth = depth


def auxiliary_widgets() -> None:
    """Add auxiliary widgets.
    """
    global game_state, start_button, val_state, canvas, p_1, p_2, p_3, p_4, p_label

    val_state = tk.StringVar()
    val_state.set("The game is ongoing")
    game_state = tk.Label(window, textvariable=val_state, font=('Arial', 20), width=30,
                          height=2)
    game_state.place(x=700, y=650, anchor='nw')

    anime_1 = Image.open("Pictures/1.png")
    anime_2 = Image.open("Pictures/2.png")
    anime_3 = Image.open("Pictures/3.png")
    anime_4 = Image.open("Pictures/4.png")

    anime_1 = anime_1.resize((300, 400), Image.ANTIALIAS)
    anime_2 = anime_2.resize((300, 400), Image.ANTIALIAS)
    anime_3 = anime_3.resize((300, 400), Image.ANTIALIAS)
    anime_4 = anime_4.resize((300, 400), Image.ANTIALIAS)

    p_1 = ImageTk.PhotoImage(anime_1)
    p_2 = ImageTk.PhotoImage(anime_2)
    p_3 = ImageTk.PhotoImage(anime_3)
    p_4 = ImageTk.PhotoImage(anime_4)

    p_label = tk.Label(window, image=p_1)
    p_label.image = p_1
    p_label.place(x=700, y=250)

    start_button = tk.Button(window, text="Restart", width=15, height=2, command=restart)
    start_button.place(x=800, y=700, anchor='nw')

    decorations = tk.Canvas(window, height=150, width=250, bg='white')
    decorations.place(x=750, y=100, anchor='nw')
    decorations.create_oval(5, 15, 120, 135,  fill='silver')
    decorations.create_oval(85, 15, 205, 135, fill='black')

    n_img = Image.open("Pictures/five_in_a_row.png")
    n_img = n_img.resize((600, 80), Image.ANTIALIAS)
    my_nimg = ImageTk.PhotoImage(n_img)

    label_1 = tk.Label(image=my_nimg)
    label_1.image = my_nimg
    label_1.place(x=620, y=25)
    # panel_1 = tk.Label(canvas, image=my_nimg)
    # panel_1.place(x=670, y=50)

    # name = tk.Label(window, text="Five in a row", font=('Helvetica', 40), width=15, heigh=1)
    # name.place(x=670, y=50)


def init(depth: int) -> None:
    """Initialize the screen.
    """
    global white_number, black_number, window, canvas, game, ai, canvas
    white_number = 0
    black_number = 0

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
    ai.depth = depth

    # Auxiliary Button.
    auxiliary_widgets()

    canvas.bind('<Button-1>', take_move)
    canvas.bind('<ButtonRelease-1>', ai_move)


def clear_0() -> None:
    """clear the window for the start of the game.
    """
    global canvas, b_0, b_1
    canvas.destroy()
    # canvas = tk.Canvas(window, width=1200, height=800)
    # b_0.destroy()
    # b_1.destroy()
    init(2)


def clear_1() -> None:
    """clear the window for the start of the game.
    """
    global canvas, b_0, b_1
    canvas.destroy()
    # canvas = tk.Canvas(window, width=1200, height=800)
    # b_0.destroy()
    # b_1.destroy()
    init(4)


def rule() -> None:
    """Initialize the GUI for rules and choosing difficulty levels.
    """
    global window, canvas, b_0, b_1, panel, img
    img = ImageTk.PhotoImage(Image.open("background_00.png"))
    canvas = tk.Canvas(window, width=1200, height=800, bg='blue')
    canvas.place(x=0, y=0, anchor='nw')

    panel = tk.Label(canvas, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    canvas.create_image(0, 0, anchor='nw', image=img)

    easy_img = tk.PhotoImage("Pictures/easy.png")
    hard_img = tk.PhotoImage("Pictures/hard.png")

    b_0 = tk.Button(canvas, command=restart, image=easy_img)
    b_0.place(x=700, y=500, anchor='nw')
    b_1 = tk.Button(canvas, command=restart, image=hard_img)
    b_1.place(x=700, y=600, anchor='nw')


if __name__ == '__main__':
    """Visualize the chess game.
    """
    # global b_0, b_1
    window = tk.Tk()
    window.title('Five in A Row Game')
    window.geometry('1200x800')

    # tutorial = tk.Label(window, text=text, font=('Arial', 25), width=70, height=12)
    # tutorial.pack()

    # rule()
    # img = ImageTk.PhotoImage(Image.open("background_00.png"))
    img = Image.open("background_00.png")
    img = img.resize((1200, 800), Image.ANTIALIAS)
    my_img = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(window, width=1200, height=800, bg='blue')
    canvas.place(x=0, y=0, anchor='nw')

    panel = tk.Label(canvas, image=my_img)
    panel.pack(side="bottom", fill="both", expand="yes")
    canvas.create_image(0, 0, anchor='nw', image=my_img)

    i_0 = Image.open("Pictures/easy.png")
    i_1 = Image.open("Pictures/hard.png")
    i_0 = i_0.resize((150, 80), Image.ANTIALIAS)
    i_1 = i_1.resize((150, 80), Image.ANTIALIAS)

    m_0 = ImageTk.PhotoImage(i_0)
    m_1 = ImageTk.PhotoImage(i_1)

    b_0 = tk.Button(canvas, command=clear_0, image=m_0)
    b_0.place(x=400, y=600, anchor='nw')
    b_1 = tk.Button(canvas, command=clear_1, image=m_1)
    b_1.place(x=700, y=600, anchor='nw')

    window.mainloop()
