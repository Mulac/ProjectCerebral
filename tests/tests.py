import unittest

from boards.tttBoard import TicTacToe
from boards.board import Player


class TestTTT(unittest.TestCase):

    def test_possible_moves(self):
        empty = TicTacToe()
        one = TicTacToe(board=[[Player.HUMAN, Player.HUMAN, Player.EMPTY],
                               [Player.HUMAN, Player.HUMAN, Player.HUMAN],
                               [Player.HUMAN, Player.HUMAN, Player.HUMAN]])
        self.assertEqual(9, len(empty.possible_moves()))
        self.assertEqual([(0, 2)], one.possible_moves())


class TestNegamax(unittest.TestCase):

    def test_negamax(self):
        empty = TicTacToe()
        one = TicTacToe(board=[[Player.HUMAN, Player.HUMAN, Player.EMPTY],
                               [Player.HUMAN, Player.HUMAN, Player.HUMAN],
                               [Player.HUMAN, Player.HUMAN, Player.HUMAN]])
        self.assertEqual(9, len(empty.possible_moves()))
        self.assertEqual([(0, 2)], one.possible_moves())


if __name__ == '__main__':
    unittest.main()
