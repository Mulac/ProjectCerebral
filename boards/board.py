from enum import Enum, auto
import abc 


class Player(Enum):
    EMPTY = auto()
    HUMAN = auto()
    COMPUTER = auto()


class Board():

    def __init__(self):
        self.board = None
        self.isects = None

    def next_player(self):
        return Player(self.move % 2 + 2)

    def update_board(self, brd):
        self.board = brd
        self.move += 1

    @abc.abstractmethod
    def is_valid_move(self, brd):
        return

    @abc.abstractmethod
    def is_end(self):
        return

    @abc.abstractmethod
    def build_board(self, isects):
        return

    @abc.abstractmethod
    def compute_state(self, counters):
        return

    @abc.abstractmethod
    def show(self):
        return
