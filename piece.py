"""..."""
from __future__ import annotations
from typing import Optional, Union
from copy import deepcopy
import math
# import random


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
    neighbours: dict[str, list[tuple[int, Piece]]]
    coordinate: tuple[int, int]

    def __init__(self, coordinate: tuple[int, int], kind: str) -> None:
        self.coordinate = coordinate
        self.kind = kind
        for direction in DIRECTIONS:
            self.neighbours[direction] = []

    def add_neighbour(self, other: Piece, direction: str, distance: int) -> None:
        """Add a new neighbour to the current piece.
        """
        self.neighbours[direction].append((distance, other))

    def is_adjacent(self, other: Piece) -> bool:
        """Return whether a piece is adjacent to current one.
        """
        cur_cor = self.coordinate
        other_cor = other.coordinate
        if abs(cur_cor[0] - other_cor[0]) <= 1 and abs(cur_cor[1] - other_cor[1]) <= 1:
            return True
        else:
            return False

    def prune_neighbours(self) -> None:
        """Adjust the neighbours when it's different color.
        """
        for direction in DIRECTIONS:
            counter = []
            for piece_tup in self.neighbours[direction]:
                if piece_tup[1].kind != self.kind:
                    counter.append(piece_tup)

            if len(counter) == 2 and counter[0][0] + counter[1][0] > 3:
                # Delete one neighbour.
                delete_one = max(counter)
                self.neighbours[direction].remove(delete_one)


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

        # Add current piece's neighbours
        self.get_neighbours(piece.coordinate)
        piece.prune_neighbours()

        for direction in DIRECTIONS:
            assert len(piece.neighbours[direction]) <= 2

    def get_neighbours(self, coordinate: tuple[int, int]) -> None:
        """Return the neighbours of given pieces according to criteria as below:
          - count pieces within 5 grids away from current coordinate in each direction.
          -
        """
        cur_piece = self.vertices[coordinate]
        cur_cor = cur_piece.coordinate

        for direction in DIRECTIONS:
            # In vertical case, only the y value changes, the distance between pieces is the
            # difference between y values.
            if direction == 'vertical':
                for i in [1, -1]:
                    for j in range(1, 6):
                        y = cur_cor[1] + i * j
                        x = cur_cor[0]
                        if (x, y) not in self.vertices:
                            continue
                        elif self.vertices[(x, y)].kind == cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    abs(y - cur_cor[1]))
                            break
                        elif self.vertices[(x, y)].kind != cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    - abs(y - cur_cor[1]))
                            break

            # In horizontal case, only x value changes, the distance between pieces is the
            # difference between x values.
            elif direction == 'horizontal':
                for i in [1, -1]:
                    for j in range(1, 6):
                        y = cur_cor[0]
                        x = cur_cor[0] + i * j
                        if (x, y) not in self.vertices:
                            continue
                        elif self.vertices[(x, y)].kind == cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    abs(x - cur_cor[0]))
                            break
                        elif self.vertices[(x, y)].kind != cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    - abs(x - cur_cor[0]))
                            break

            # In right diagonal case, x y changes simultaneously, so the distance between
            # piece could be either one.
            elif direction == 'right diagonal':
                for i in [1, -1]:
                    for j in range(1, 6):
                        y = cur_cor[0] + i * j
                        x = cur_cor[0] + i * j
                        if (x, y) not in self.vertices:
                            continue
                        elif self.vertices[(x, y)].kind == cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    abs(x - cur_cor[0]))
                            break
                        elif self.vertices[(x, y)].kind != cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    - abs(x - cur_cor[0]))
                            break

            # In right diagonal case, x y changes simultaneously, so the distance between
            # piece could be either one.
            elif direction == 'left diagonal':
                for i in [1, -1]:
                    for j in range(1, 6):
                        y = cur_cor[0] + i * j
                        x = cur_cor[0] - i * j
                        if (x, y) not in self.vertices:
                            continue
                        elif self.vertices[(x, y)].kind == cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    abs(x - cur_cor[0]))
                            break
                        elif self.vertices[(x, y)].kind != cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    - abs(x - cur_cor[0]))
                            break

    def evaluate(self) -> int:
        """Return the score of the current situation.
        An empty set need to be passed in.
        """
        # ACCUMULATOR:
        score_so_far = 0

        for coordinate in self.vertices:
            for direc in DIRECTIONS:
                score_so_far += self._single_evaluation(coordinate, 4, direc)

        return score_so_far

    def _single_evaluation(self, coordinate: tuple[int, int], count: int, direction: str) \
            -> Union[float, int]:
        """...

        """
        # ACCUMULATOR:
        score_so_far = 0

        current_piece = self.vertices[coordinate]
        neighbours = current_piece.neighbours

        pieces_in_dir = neighbours[direction]

        # The number of enemy pieces.
        counter = 0

        # Using a list to store the distance between pieces in terms of [1, 2,...]
        length = []

        for piece in pieces_in_dir:

            # If enemy piece is countered, add 1 to counter.
            if piece[1].kind != current_piece.kind:
                counter += 1

            elif count > 0 and piece[0] < count:  # Make sure that the length if enough.

                # Update the length only if it's the same kind piece
                length.append(piece[0])
                count -= piece[0]

                # Five in a row.
                if all(item == 1 for item in length) and count == 0:
                    if current_piece.kind == 'black':
                        score_so_far += math.inf
                        return score_so_far
                    else:
                        score_so_far += -1 * math.inf
                        return score_so_far

                score_so_far += self._get_score(counter, length)

                # Make a copy of the piece we want to evaluate next, and remove the edge
                # between current piece and this copied piece so that it won't loop on the
                # same edge.
                next_piece = deepcopy(piece[1])
                next_piece.neighbours[direction].remove((piece[0], current_piece))

                score_so_far += self._single_evaluation(next_piece.coordinate, count, direction)

        return score_so_far

    def _get_score(self, counter: int, length: list[int]) -> int:
        """..."""
        score_so_far = 0

        if counter >= 2:
            # If there are two enemy pieces, there's no change that row in a row could be
            # achieved in this direction
            pass
        else:
            for grid_len in length:
                if grid_len == 1:
                    score_so_far += 400
                elif grid_len == 2:
                    score_so_far += 100
                elif grid_len == 3:
                    score_so_far += 25
            if counter == 1:
                score_so_far = score_so_far // 2

        return score_so_far







