"""..."""
from __future__ import annotations
from typing import Optional


DIRECTIONS = {'above', 'below', 'right', 'left', 'top right', 'top left',
              'bottom right', 'bottom left'}


class Piece:
    """A piece of chess which can be either black or white.

      Instance Attributes:
        - kind: represent the kind of the piece which could be 'black' or 'white'
        - neighbours: Storing the neighbouring pieces using a dictionary from direction to Piece.
        - coordinate: The coordinate of this piece

      Representation Invariants:
        - kind in {'black', 'white'}
        - all(neighbour in {'above', 'below', 'right', 'left', 'top right', 'top left',
         'bottom right', 'bottom left'})
      """
    kind: str
    neighbours: dict[str, Piece]
    obstacles: dict[str, Piece]
    coordinate: tuple[int, int]

    def __init__(self, coordinate: tuple[int, int], kind: str) -> None:
        self.coordinate = coordinate
        self.kind = kind
        self.neighbours = {}
        self.obstacles = {}


class Pieces:
    """A graph that represents the whole game pieces.

    Instance Attributes:
      - vertices: Store all the piece using a dictionary from coordinate to piece.
    """
    vertices: dict[tuple[int, int], Piece]

    def __init__(self) -> None:
        self.vertices = {}

    def add_piece(self, piece: Piece) -> Optional[int]:
        """Add a piece to the graph. And then add edge to its surrounding pieces,
        which update the neighbours and obstacles attribute.

        If the piece is on a coordinate that has already been taken, return -1.
        """
        if piece.coordinate in self.vertices:
            # Invalid input
            print('This spot has already been occupied')
            return -1

        self.vertices[piece.coordinate] = piece
        all_neighbours = self.get_neighbours(piece.coordinate)

        for direction in all_neighbours:
            if all_neighbours[direction].kind == piece.kind:
                piece.neighbours[direction] = all_neighbours[direction]
            else:
                piece.obstacles[direction] = all_neighbours[direction]

    def get_neighbours(self, coordinate: tuple[int, int]) -> dict[str, Piece]:
        """Return the neighbours of given pieces.
        """

    def evaluate(self) -> int:
        """Return the score of the current situation.
        """

    def _pieces_in_a_line(self, c1: tuple[int, int]) -> list[Piece]:
        """Return the piece in a line with the same color.
        """
