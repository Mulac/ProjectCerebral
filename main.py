import sys
import time

from robot.boards.nmmBoard import NineMensMorris
from robot.boards.tttBoard import TicTacToe
from robot.control import make_tictactoe_move
from robot.helper import Player
from robot.negamax import decision
from robot.vision import Vision

corners = None
computer_turn = False


def play():
    global computer_turn
    
    vision.update()

    # counters is now a dictionary mapping from logical position to pixel 'Position'
    board, counters = game.compute_state(vision.counters)
    if game.is_valid_move_state(board):
        game.update_board(board)
        game.show()

    # Make computer move
    if game.player == Player.HUMAN and not computer_turn:
        computer_turn = True

    if computer_turn and game.player == Player.COMPUTER:
        move = decision(game, 20)
        print(move)
        computer_turn = False
        make_tictactoe_move(move, counters)


    winner = game.is_end()
    if winner:
        print("\nThe Winner is: {}".format(winner))
        return False
    return True


if __name__ == "__main__":
    game = TicTacToe()             # Create the board game
    vision = Vision()

    vision.detect_board(game)

    while play():
        if vision.cv2.waitKey(1) & 0xFF == ord('q'):
            break
