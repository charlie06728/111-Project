"""A ChessGame class"""
from piece import Piece, Pieces


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

    def __init__(self, board: list[list], is_black_active: bool = True) -> None:
        """Initialize the Game"""
        self._board = board
        self._is_black_active = is_black_active
        self.pieces = Pieces()

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

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Return a list of valid moves.
        """

    def get_score(self) -> int:
        """Return the socre of current situation.
        """
        return self.pieces.evaluate()
