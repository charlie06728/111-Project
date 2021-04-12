"""The file that run the game."""

from ChessGame import ChessGame
from piece import Piece, Pieces
from Gametree import GameTree
from typing import Optional
import random


class NormalPlayer:
    """A player that would only take next move near friendly pieces.

    Instance Attribute:
      - kind: The piece kind of this player, black or white
      - game_tree: The game tree that two player shares.
      - game: The game of this Chess play.
      - prev_move: previous move of this player.

    Representation Invariants:
      - kind in {'black', 'white'}
    """
    kind: str
    game_tree: GameTree
    game: ChessGame
    prev_move: Optional[tuple[int, int]]

    def __init__(self, kind: str, game: ChessGame) -> None:
        self.kind = kind
        self.game_tree = None
        self.game = game
        self.prev_move = None

    def choose_move(self) -> tuple[int, int]:
        """choose a move that near the previous move.
        """
        valid_moves = self.game.get_valid_moves()
        if self.kind == 'black' and self.prev_move is None:
            # Center of the board
            return (8, 8)
        elif self.kind == 'white' and self.prev_move is None:
            return random.choice(valid_moves)
        else:
            i = random.choice([0, 1, -1])
            j = random.choice([0, 1, -1])
            move = (self.prev_move[0] + i, self.prev_move[1] + j)
            while move not in valid_moves:
                i = random.choice([0, 1, -1])
                j = random.choice([0, 1, -1])
                move = (self.prev_move[0] + i, self.prev_move[1] + j)

            self.prev_move = move

            return move


class IntelligentPlayer:
    """AI that could play wisely.

    Instance Attribute:
      - kind: the piece kind of this player.
      - game_tree: the game tree
      - game: The Chess game
      - prev_move: The previous move of opposite player.

    Representation Invariants:
      -
    """
    kind: str
    game_tree: Optional[GameTree]
    game: ChessGame
    prev_move: Optional[tuple[int, int]]
    depth: int

    def __init__(self, kind: str, game: ChessGame, depth: int = 2) -> None:
        self.kind = kind
        self.game_tree = None
        self.game = game
        self.prev_move = None
        self.depth = depth

    def choose_move(self) -> tuple[int, int]:
        """Choose next move wisely.
        """
        prev_move = self.game.prev_move
        self.game_tree = GameTree()
        self.game_tree.generate_tree_based_on_move(self.game, prev_move, self.depth)
        if self.kind == 'black':
            # assert self.game_tree.subtrees == []
            cur_tree = self.game_tree.subtrees[0]
            cur_max = self.game_tree.subtrees[0].score
            for subtree in self.game_tree.subtrees:
                if subtree.score > cur_max:
                    cur_tree = subtree
                    cur_max = subtree.score
        else:
            cur_tree = self.game_tree.subtrees[0]
            cur_min = self.game_tree.subtrees[0].score
            for subtree in self.game_tree.subtrees:
                if subtree.score < cur_min:
                    cur_tree = subtree
                    cur_min = subtree.score

        return cur_tree.root
