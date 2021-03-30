"""..."""
from __future__ import annotations
from typing import Optional
import math


# DIRECTIONS = {'above', 'below', 'right', 'left', 'top right', 'top left',
#               'bottom right', 'bottom left'}
DIRECTIONS = {'vertical', 'horizontal', 'right diagonal', 'left diagonal'}


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
    neighbours: dict[str, list[Piece]]
    obstacles: dict[str, list[Piece]]
    coordinate: tuple[int, int]

    def __init__(self, coordinate: tuple[int, int], kind: str) -> None:
        self.coordinate = coordinate
        self.kind = kind
        self.neighbours = {}
        self.obstacles = {}

    def is_adjacent(self, other: Piece) -> bool:
        """Return whether a piece is adjacent to current one.
        """
        cur_cor = self.coordinate
        other_cor = other.coordinate
        if abs(cur_cor[0] - other_cor[0]) <= 1 and abs(cur_cor[1] - other_cor[1]) <= 1:
            return True
        else:
            return False


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
            for item in all_neighbours[direction]:
                if item.kind == piece.kind:
                    if direction in piece.neighbours:
                        piece.neighbours[direction].append(item)
                    else:
                        piece.neighbours[direction] = [item]
                else:
                    if direction in piece.obstacles:
                        piece.obstacles[direction].append(item)
                    else:
                        piece.obstacles = [item]

    def get_neighbours(self, coordinate: tuple[int, int]) -> dict[str, list[Piece]]:
        """Return the neighbours of given pieces.
        """
        # TODO:

    def evaluate(self, visited: set[Piece]) -> int:
        """Return the score of the current situation.
        """
        # ACCUMULATOR:
        score_so_far = 0

        for coordinate in self.vertices:
            visited += self.vertices[coordinate]

    def _single_evaluation(self, coordinate: tuple[int, int], visited: set[Piece]) \
            -> tuple[int, set]:
        """...
        current_piece = self.vertices[coordinate]
        visited.add(self.vertices[coordinate])
        neighbours = self.get_neighbours(current_piece.coordinate)
        current_length = 5
        score = 0
        for direction in DIRECTIONS:
            if direction in neighbours:
                pieces_in_direction = neighbours[direction]
                for piece in pieces_in_direction:
                    # If the neighbouring piece doesn't have the same color, no score change will
                    # be made
                    if piece.kind == current_piece.kind and piece.kind == 'black':
                        score += 50
                    elif piece.kind == current_piece.kind and piece.kind == 'white':
                        score -= 50
                    visited.add(piece)
                    score += self._single_evaluation(piece.coordinate, visited)

        return score
        """
        current_piece = self.vertices[coordinate]
        visited.add(current_piece)
        neighbours = self.get_neighbours(coordinate)
        score_so_far = 0
        for direction in DIRECTIONS:
            pieces_in_dir = neighbours[direction]
            favor_pieces = {current_piece}
            for piece in pieces_in_dir:
                counter_pieces = set()
                if piece.kind == current_piece:
                    favor_pieces.add(piece)
                elif piece.kind != current_piece:
                    counter_pieces.add(piece)

                if len(counter_pieces) == 2:
                    # This line has no possibility of being five in a row.
                    score_so_far = 0
                else:
                    score_so_far += self._get_score(favor_pieces, counter_pieces)

        return (score_so_far, visited)

    def _get_score(self, pieces: set[Piece], obstacles: set[Piece]) -> int:
        """Return the score of this line.
        """
        length = len(pieces)
        obs_length = len(obstacles)
        assert obs_length < 2
        score = 0
        if length == 1:
            score = 50 - 25 * obs_length
        elif length == 2 and obs_length == 0:
            score = 200 - 100 * obs_length
        elif length == 3 and obs_length == 0:
            score = 500 - 200 * obs_length
        elif length == 4:
            if self._in_a_line(pieces):
                score = 8000
            else:
                score = 800 - 300 * obs_length
        elif length == 5:
            # win
            score = math.inf

        return score

    def _in_a_line(self, pieces: set[Piece]) -> bool:
        """Return whether these pieces is in a line without gap.
        """
        co = pieces
        for piece in pieces:
            co.remove(piece)
            for neighbour in co.copy():
                if piece.is_adjacent(neighbour):
                    co.remove(neighbour)

        return len(co) == 0
