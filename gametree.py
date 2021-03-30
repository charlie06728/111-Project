"""The gametree class for the five in a row project"""

from __future__ import annotations
from typing import List, Optional
import ChessGame

START_MOVE = '*'

class GameTree:
    """A decision tree for the five in a row game.
    - attributes:
    - score: int, representing the corresponding score for the location on the board
    - move: str, representing the position on the board
    - white_move: bool, whether the current depth of moves is for white or black player
    - subtrees: list[gametree], the possible moves after this move
    - better_score: int, the best possible score currently for the tree.
    Update the score if a step earns more score than before

    """
    score: int
    move: str
    black_move: bool
    subtrees: List[GameTree]
    better_score: int
    game_status: ChessGame.ChessGame

    def __init__(self, score: int = 0, move: str = '*', black_move: bool = True,
                 better_score: int = 0):
        """Initialize the gametree to be an empty tree. """
        self.score = score
        self.move = move
        self.black_move = black_move  # In start of the game, black player moves first
        self.subtrees = []
        self.better_score = better_score
        self.game_status = ChessGame.ChessGame()

    def generate_tree_based_on_move(self, game_state: ChessGame, prev_move: str,
                                    depth: int = 0) -> GameTree:
        """ A recursive function that returns a tree.
        The root of the tree will be prev_move. The tree will first get all possible next moves,
        and for each "next move", it will recursively look for next moves of the move, and stop
        when the depth is 5. Each time the tree adds a subtree, it also re-calculates the
        score for the move. When calculating score, once we find that the score is worse than
        self.current_score, we move on to the next immediately. When the move is for our ai, it
        will seek largest score, and when the move is for opponent, it will seek the lowest score.
        """
        if depth >= 5:
            return self
        else:
            ...

    def add_subtree(self, subtree: GameTree) -> None:
        """Add the given subtree to self.subtrees. """
        self.subtrees.append(subtree)
        self.update_score()

    def update_score(self) -> None:
        """Update the score for the current tree based on the given chess game. """
        self.score = ChessGame.ChessGame.get_score(self.game_status)

    def get_subtrees(self) -> Optional[List[GameTree]]:
        """Return all subtrees of the tree. If there is no subtrees, return None. """
        if self.subtrees == []:
            return None
        else:
            return self.subtrees

    def find_subtree_by_move(self, move: str) -> Optional[GameTree]:
        """Return the found subtree by the given move. Return None if no subtree is found. """
        for subtree in self.subtrees:
            if move == subtree.move:
                return subtree
        return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ...
