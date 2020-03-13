import sys
import vision
from negamax import negamax
from boards.tttBoard import TicTacToe
from boards.nmmBoard import NineMensMorris

corners = None


def setup():
    global corners
    ret, img = cap.read()

    # Find the corners to transform the camera frames
    if corners is None and isinstance(game, NineMensMorris):
        corners = game.build_board(vision.find_board, img)
    else:
        raise Exception("Please show me NMM board first")

    # Find the new relative intersections of the board
    game.build_board(vision.find_board, vision.deskew(img, corners))


def play(representation):
    # representation.show()
    ret, frame = cap.read()
    frame = vision.deskew(frame, corners)

    counters, cimg = vision.find_counters(frame)
    if counters is not None:  # Counters have started being placed
        board = representation.compute_state(counters)
        if representation.is_valid_move_state(board):
            representation.update_board(board)
            representation.show()

    # Display the resulting frame
    vision.cv2.imshow('counters', cimg)

    winner = representation.is_end()
    if winner:
        print("\nThe Winner is: {}".format(winner))
        return False
    return True


if __name__ == "__main__":
    game = NineMensMorris()             # Create the board game
    cap = vision.cv2.VideoCapture(0)    # Open the camera

    setup()

    while play(game):
        if vision.cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()                       # Close the camera
    vision.cv2.destroyAllWindows()      # Close all windows
