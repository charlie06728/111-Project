"""A ChessGame class"""
from piece import Piece, Pieces
from typing import Optional

BOARD_WIDTH = 15
BOARD_LENGTH = 15


class ChessGame:
    """A class representing a state of a game.

    Representation Invariants:
      -
    """
    # Private Attributes:
    #  - _board: a two-dimensional representation of a 15x15 chess board, storing the value of
    # 'black', 'white' and None
    #  - _valid_moves: a list of the valid moves of the current player
    #  - _is_black_active: a boolean representing whether black is the current player
    _board: list[list]
    _valid_moves: list[str]
    _is_black_active: bool
    pieces: Pieces
    prev_moves: Optional[tuple[int, int]]

    def __init__(self, is_black_active: bool = True) -> None:
        """Initialize the Game"""
        self._board = []
        for i in range(15):
            self._board.append([])
            for _ in range(15):
                self._board[i].append(None)

        self._is_black_active = is_black_active
        self.pieces = Pieces()
        self.prev_moves = None

    def make_move(self, coordinate: tuple[int, int]) -> None:
        """Make move on the chess game.
        """
        if self._is_black_active:
            player = 'black'
        else:
            player = 'white'

        new_piece = Piece(coordinate, player)
        self.pieces.add_piece(new_piece)
        self._board[coordinate[0]][coordinate[1]] = player

        self.prev_moves = coordinate

    def check_surrounding(self, piece: tuple[int, int], valid_moves: list) -> list[tuple[int, int]]:
        """Helper for get_valid_moves, checks the 5 by 5 surrounding of a piece and return the
        unfilled positions. """
        moves_for_piece = []
        for i in range(piece[0] - 3, piece[0] + 4):
            for j in range(piece[1] - 2, piece[1] + 3):
                if i in range(0, BOARD_WIDTH + 1) and j in range(0, BOARD_LENGTH + 1):
                    if self._board[i][j] is None and (i, j) not in valid_moves:
                        moves_for_piece.append((i, j))

        return moves_for_piece

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Return a list of valid moves. When there is no valid moves, return an empty list.

        NOTE: notice that when the board is empty, this function also returns an empty list.
        So when making a move, make sure to check if previous_move is '*', and set the first
        piece directly at the centre of the board.
        """
        valid_moves = []
        for row in self._board:
            for piece in row:
                if piece is not None:  # if there is a piece
                    valid_moves.extend(self.check_surrounding(piece, valid_moves))

        return valid_moves

    def get_score(self) -> int:
        """Return the score of current situation.
        """
        return self.pieces.evaluate()

    def get_is_black(self) -> bool:
        """Return whether the current move is by black.
        """
        return self._is_black_active
