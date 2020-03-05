from enum import Enum, auto
import abc 


class Player(Enum):
    EMPTY = 0
    HUMAN = 1
    COMPUTER = 2


class Board:

    def __init__(self):
        self.board = None
        self.move = 0
        self.player = Player.HUMAN
        self.isects = None

    def next_player(self):
        if self.player == Player.HUMAN:
            return Player.COMPUTER
        return Player.HUMAN

    def switch_player(self):
        self.player = self.next_player()

    def update_board(self, brd):
        self.board = brd
        self.switch_player()
        self.move += 1

    @abc.abstractmethod
    def play_move(self, move):
        return

    @abc.abstractmethod
    def is_end(self):
        return

    @abc.abstractmethod
    def is_valid_move_state(self, brd):
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
