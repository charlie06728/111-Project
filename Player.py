"""The file that run the game."""

from ChessGame import ChessGame
from Gametree import GameTree
from typing import Optional


class IntelligentPlayer:
    """AI that could play wisely.

    Instance Attribute:
      - kind: the piece kind of this player.
      - game_tree: the game tree
      - game: The Chess game
      - prev_move: The previous move of opposite player.
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
