from enum import Enum, auto
import abc 


class Player(Enum):
    EMPTY = auto()
    HUMAN = auto()
    COMPUTER = auto()


class Board():

    def __init__(self):
        self.board = None
        self.move = 0
        self.isects = None

    def nextPlayer(self):
        return Player(self.move % 2 + 2)

    def updateBoard(self, brd):
        self.board = brd
        self.move += 1

    @abc.abstractmethod
    def isValidMove(self, brd):
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
