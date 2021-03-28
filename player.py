"""The player class for the five in a row project"""

from typing import Optional
import Gametree
import ChessGame


class Player:
    """ A class for how two players move their pieces during the game
        - attributes:
        - gametree: Gametree
    """


def __init__(self, name, symbol):
    self.name = name
    self.symbol = symbol


def start_move(self, game):
    """ Update the first piece places on the chess broad, which will
    be in the middle of the chess broad.
    """


def make_move(self, game_state: ChessGame, prev_move: str) -> str:
    """ Return a string representing the next move to be made by the ai,
    based on the previous move of opponent. The function will generate
    a gametree of depth 5, look for the left most subtree that has
    the highest score, and return the move (position on the board)
    corresponding to that subtree.
    """
