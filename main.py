import sys
import time
import robot.vision as vision
from robot.negamax import decision
from robot.control import make_tictactoe_move
from robot.helper import Player
from robot.boards.tttBoard import TicTacToe
from robot.boards.nmmBoard import NineMensMorris

corners = None
computer_turn = False

def setup(game):
    global corners

    found = False       # Keep trying to find board until 4 intersections found
    while not found:
        ret, img = cap.read()

        # Find the corners to transform the camera frames
        if corners is None:
            found, corners = game.build_board(vision.find_board, img)

        # Find the new relative intersections of the board
        found, _ = game.build_board(vision.find_board, vision.deskew(img, corners))


def play(representation):
    global computer_turn
    ret, frame = cap.read()
    frame = vision.deskew(frame, corners)

    # Update board
    counters, cimg = vision.find_counters(frame)
    if counters is not None:  # Counters have started being placed
        # counters is now a dictionary mapping from logical position to pixel 'Position'
        board, counters = representation.compute_state(counters)
        if representation.is_valid_move_state(board):
            representation.update_board(board)
            representation.show()

    # Make computer move
    if representation.player == Player.HUMAN and not computer_turn:
        computer_turn = True

    if computer_turn and representation.player == Player.COMPUTER:
        move = decision(representation, 20)
        print(move)
        computer_turn = False
        # make_tictactoe_move(move, counters)



    # Display the frame with counter positions
    vision.cv2.imshow('counters', cimg)

    winner = representation.is_end()
    if winner:
        print("\nThe Winner is: {}".format(winner))
        return False
    return True


if __name__ == "__main__":
    reference = TicTacToe()             # Create the board game
    cap = vision.cv2.VideoCapture(0)    # Open the camera

    setup(reference)

    # while True:
    #     if vision.cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # g = TicTacToe()
    # setup(g)

    while play(reference):
        if vision.cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()                       # Close the camera
    vision.cv2.destroyAllWindows()      # Close all windows
