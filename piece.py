"""..."""
from __future__ import annotations
from typing import Optional, Union
from copy import deepcopy, copy
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
        self.neighbours = {}
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
            neigh = self.neighbours[direction]
            if len(neigh) == 0:
                return
            for piece_tup in self.neighbours[direction]:
                if piece_tup[1].kind != self.kind:
                    counter.append(piece_tup)

            if len(counter) == 2 and counter[0][0] + counter[1][0] < -3:
                # Delete one neighbour.
                assert isinstance(counter[0][0], int)
                assert counter[0][0] < 0
                lst = [p[0] for p in counter]
                delete_one = min(lst)
                index = lst.index(delete_one)
                self.neighbours[direction].remove(counter[index])
            # elif len(counter) == 1 and counter[0][0] < -1:
            #     self.neighbours[direction].remove(counter[0])


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
                    for j in range(1, 4):
                        y = cur_cor[1] + i * j
                        x = cur_cor[0]
                        if (x, y) not in self.vertices:
                            continue
                        elif self.vertices[(x, y)].kind == cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    abs(y - cur_cor[1]))
                            self.vertices[(x, y)].add_neighbour(cur_piece, direction,
                                                                abs(y - cur_cor[1]))
                            for original_nei in self.vertices[(x, y)].neighbours[direction]:
                                # breakpoint()
                                n_p = self.vertices[(x, y)]
                                # if original_nei[1].kind != n_p.kind:
                                #     continue
                                if abs(original_nei[0]) > abs(y - cur_cor[1]) and \
                                        ((y - cur_piece.coordinate[1]) /
                                         (y - original_nei[1].coordinate[1])) > 0:
                                    n_p.neighbours[direction].remove(original_nei)
                                    # breakpoint()
                                    # n_p.add_neighbour(cur_piece, direction, abs(y - cur_cor[1]))
                            break
                        elif self.vertices[(x, y)].kind != cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    - abs(y - cur_cor[1]))
                            self.vertices[(x, y)].add_neighbour(cur_piece, direction,
                                                                - abs(y - cur_cor[1]))
                            for original_nei in self.vertices[(x, y)].neighbours[direction]:
                                n_p = self.vertices[(x, y)]
                                if abs(original_nei[0]) > abs(y - cur_cor[1]) and (
                                        (y - cur_piece.coordinate[1]) /
                                        (y - original_nei[1].coordinate[1])) > 0:
                                    n_p.neighbours[direction].remove(original_nei)
                                    # n_p.prune_neighbours()
                            break

            # In horizontal case, only x value changes, the distance between pieces is the
            # difference between x values.
            elif direction == 'horizontal':
                for i in [1, -1]:
                    for j in range(1, 4):
                        y = cur_cor[1]
                        x = cur_cor[0] + i * j
                        if (x, y) not in self.vertices:
                            continue
                        elif self.vertices[(x, y)].kind == cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    abs(x - cur_cor[0]))
                            self.vertices[(x, y)].add_neighbour(cur_piece, direction,
                                                                abs(x - cur_cor[0]))
                            for original_nei in self.vertices[(x, y)].neighbours[direction]:
                                # breakpoint()
                                n_p = self.vertices[(x, y)]
                                # if original_nei[1].kind != n_p.kind:
                                #     continue
                                if abs(original_nei[0]) > abs(x - cur_cor[0]) and \
                                        ((x - cur_piece.coordinate[0]) /
                                         (x - original_nei[1].coordinate[0])) > 0:
                                    n_p.neighbours[direction].remove(original_nei)
                                    # breakpoint()
                                    # n_p.add_neighbour(cur_piece, direction, abs(x - cur_cor[0]))
                            break
                        elif self.vertices[(x, y)].kind != cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    - abs(x - cur_cor[0]))
                            self.vertices[(x, y)].add_neighbour(cur_piece, direction,
                                                                - abs(x - cur_cor[0]))
                            for original_nei in self.vertices[(x, y)].neighbours[direction]:
                                n_p = self.vertices[(x, y)]
                                if abs(original_nei[0]) > abs(x - cur_cor[0]) and (
                                        (x - cur_piece.coordinate[0]) /
                                        (x - original_nei[1].coordinate[0])) > 0:
                                    n_p.neighbours[direction].remove(original_nei)
                                    # n_p.prune_neighbours()
                            break

            # In right diagonal case, x y changes simultaneously, so the distance between
            # piece could be either one.
            elif direction == 'right diagonal':
                for i in [1, -1]:
                    for j in range(1, 4):
                        y = cur_cor[1] + i * j
                        x = cur_cor[0] + i * j
                        if (x, y) not in self.vertices:
                            continue
                        elif self.vertices[(x, y)].kind == cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    abs(x - cur_cor[0]))
                            self.vertices[(x, y)].add_neighbour(cur_piece, direction,
                                                                abs(x - cur_cor[0]))
                            for original_nei in self.vertices[(x, y)].neighbours[direction]:
                                # breakpoint()
                                n_p = self.vertices[(x, y)]

                                if abs(original_nei[0]) > abs(x - cur_cor[0]) and \
                                        ((x - cur_piece.coordinate[0]) /
                                         (x - original_nei[1].coordinate[0])) > 0:
                                    n_p.neighbours[direction].remove(original_nei)
                            break
                        elif self.vertices[(x, y)].kind != cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    - abs(x - cur_cor[0]))
                            self.vertices[(x, y)].add_neighbour(cur_piece, direction,
                                                                - abs(x - cur_cor[0]))
                            for original_nei in self.vertices[(x, y)].neighbours[direction]:
                                n_p = self.vertices[(x, y)]
                                if abs(original_nei[0]) > abs(x - cur_cor[0]) and (
                                        (x - cur_piece.coordinate[0]) /
                                        (x - original_nei[1].coordinate[0])) > 0:
                                    n_p.neighbours[direction].remove(original_nei)
                                    # n_p.prune_neighbours()
                            break

            # In right diagonal case, x y changes simultaneously, so the distance between
            # piece could be either one.
            elif direction == 'left diagonal':
                for i in [1, -1]:
                    for j in range(1, 4):
                        y = cur_cor[1] + i * j
                        x = cur_cor[0] - i * j
                        if (x, y) not in self.vertices:
                            continue
                        elif self.vertices[(x, y)].kind == cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    abs(x - cur_cor[0]))
                            self.vertices[(x, y)].add_neighbour(cur_piece, direction,
                                                                abs(x - cur_cor[0]))
                            for original_nei in self.vertices[(x, y)].neighbours[direction]:
                                # breakpoint()
                                n_p = self.vertices[(x, y)]
                                # if original_nei[1].kind != n_p.kind:
                                #     continue
                                if abs(original_nei[0]) > abs(x - cur_cor[0]) and \
                                        ((x - cur_piece.coordinate[0]) /
                                         (x - original_nei[1].coordinate[0])) > 0:
                                    n_p.neighbours[direction].remove(original_nei)
                            break
                        elif self.vertices[(x, y)].kind != cur_piece.kind:
                            cur_piece.add_neighbour(self.vertices[(x, y)], direction,
                                                    - abs(x - cur_cor[0]))
                            self.vertices[(x, y)].add_neighbour(cur_piece, direction,
                                                                - abs(x - cur_cor[0]))
                            for original_nei in self.vertices[(x, y)].neighbours[direction]:
                                n_p = self.vertices[(x, y)]
                                if abs(original_nei[0]) > abs(x - cur_cor[0]) and (
                                        (x - cur_piece.coordinate[0]) /
                                        (x - original_nei[1].coordinate[0])) > 0:
                                    n_p.neighbours[direction].remove(original_nei)
                                    # n_p.prune_neighbours()
                            break

    def evaluate(self) -> int:
        """Return the score of the current situation.
        An empty set need to be passed in.
        """
        # ACCUMULATOR:
        score_so_far = 0

        for coordinate in self.vertices:
            for direc in DIRECTIONS:
                # print(f"")
                cor_score = self._single_evaluation(coordinate, 4, direc, set(), [], [])
                if cor_score is None:
                    cor_score = 0
                elif cor_score == math.inf or cor_score == math.inf * -1:
                    return cor_score
                score_so_far += cor_score
                if score_so_far == math.inf or score_so_far == math.inf * -1:
                    return score_so_far

                # print(f"{coordinate} - {cor_score}")

        return score_so_far

    def _single_evaluation(self, coordinate: tuple[int, int], count: int, direction: str,
                           visited: set, lst: list, length: list, counter: int = 0) -> \
            Union[float, int, None]:
        """..."""
        # ACCUMULATOR:
        score_so_far = 0

        current_piece = self.vertices[coordinate]
        neighbours = current_piece.neighbours

        pieces_in_dir = neighbours[direction]
        if len(pieces_in_dir) == 0:
            return 0

        # Using a list to store the distance between pieces in terms of [1, 2,...]
        # length = []

        lst_of_length = []
        for p in pieces_in_dir:
            if p[0] > 0:
                lst_of_length.append(p[0])
        for i, piece in enumerate(pieces_in_dir.copy()):
            # Using a list to store the distance between pieces in terms of [1, 2,...]
            # length = []
            # print(f"{piece[1].coordinate}--neighbour")
            if piece[1] in visited:
                if piece[0] in lst_of_length:
                    lst_of_length.remove(piece[0])
                continue

            assert piece[1] not in visited

            # If enemy piece is countered, add 1 to counter.
            if piece[1].kind != current_piece.kind:
                if piece[0] != -1:
                    continue
                # assert piece[0] == -1
                counter += 1
                if counter == 2:
                    current_piece.neighbours[direction] = []
                    for tup in length:
                        tup[1].neighbours[direction] = []
                    return None
                elif counter == 1:
                    # score_so_far = score_so_far * ((piece[0] * -1) / (piece[0] * -1 + 1))
                    score_so_far = score_so_far * ((piece[0] * -1) / 3)
                # continue
            elif count > 0:  # Make sure that the length is enough.
                assert piece[1].kind == current_piece.kind

                if piece[0] != min(lst_of_length) and \
                        pieces_in_dir[lst_of_length.index(min(lst_of_length))][1] not in visited:
                    # Swap sequence
                    index = lst_of_length.index(min(lst_of_length))
                    pieces_in_dir[i], pieces_in_dir[index] = pieces_in_dir[index], pieces_in_dir[i]
                    piece = pieces_in_dir[i]

                if piece[0] > count:
                    continue

                # Update the length only if it's the same kind piece
                length.append(piece)
                if piece[0] == 1:
                    lst.append(1)
                # print(length)
                # print(current_piece.coordinate)
                count -= piece[0]

                # Five in a row.
                if len(lst) == 4 and count == 0:
                    # breakpoint()
                    if current_piece.kind == 'black':
                        score_so_far = math.inf
                        return score_so_far
                    else:
                        score_so_far = -1 * math.inf
                        return score_so_far
                elif len(lst) == 3 and count == 1:
                    if current_piece.kind == 'black' and counter == 0:
                        score_so_far += 4800 * 2
                    elif current_piece.kind == 'black' and counter == 1:
                        score_so_far += 1200
                    elif current_piece.kind == 'white' and counter == 0:
                        score_so_far -= 4800 * 2
                    elif current_piece.kind == 'white' and counter == 1:
                        score_so_far -= 1200
                else:
                    init_score = self._get_score(counter, length)
                    if self.vertices[coordinate].kind == 'white':
                        # breakpoint()
                        score_so_far -= init_score
                    else:
                        score_so_far += init_score
                    # score_so_far += self._get_score(counter, length)

                next_piece = piece[1]

                visited.add(current_piece)
                # print(init_score)

                n_score = self._single_evaluation(next_piece.coordinate, count, direction,
                                                  visited, lst, length, counter)
                if n_score is None:
                    return None
                score_so_far += n_score

        return score_so_far

    def _get_score(self, counter: int, length: list[tuple[int, Piece]]) -> int:
        """..."""
        score_so_far = 0

        if counter >= 2:
            # If there are two enemy pieces, there's no chance that row in a row could be
            # achieved in this direction
            pass
        else:
            for grid_len in length:
                if grid_len[0] == 1:
                    score_so_far += 800
                elif grid_len[0] == 2:
                    score_so_far += 400
                elif grid_len[0] == 3:
                    score_so_far += 100
            if counter == 1:
                score_so_far = score_so_far // 2

        return score_so_far


if __name__ == '__main__':
    ps = Pieces()
    ps.add_piece(Piece((6, 7), 'white'))
    # ps.add_piece(Piece((11, 7), 'black'))
    # ps.add_piece(Piece((8, 7), 'black'))
    ps.add_piece(Piece((7, 7), 'white'))
    ps.add_piece(Piece((8, 7), 'white'))
    ps.add_piece(Piece((9, 7), 'white'))
    ps.add_piece(Piece((10, 7), 'white'))
    # ps.add_piece(Piece((8, 7), 'black'))
    # ps.add_piece(Piece((2, 7), 'white'))
    print(ps.evaluate())
    print(ps.vertices[6, 7].neighbours)
