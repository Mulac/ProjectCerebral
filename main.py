import sys
import vision
from negamax import negamax
from boards.tttBoard import TicTacToe
from boards.nmmBoard import NineMensMorris

corners = None


def setup():
    global corners
    ret, img = cap.read()

    if isinstance(game, NineMensMorris):
        corners = game.build_board(vision.find_board, img)
    else:
        game.build_board(vision.find_board, img)


def play(representation):
    while True:
        # representation.show()
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = vision.deskew(frame, corners)

        winner = representation.is_end()
        if winner:
            print(winner, "WINS")
            break

        counters, cimg = vision.find_counters(frame)
        if counters is not None:  # Counters have started being placed
            board = representation.compute_state(counters)
            if representation.is_valid_move_state(board):
                representation.update_board(board)
                representation.show()

        # Display the resulting frame
        vision.cv2.imshow('counters', cimg)
        if vision.cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    game = NineMensMorris()

    cap = vision.cv2.VideoCapture(0)

    setup()
    play(game)

    # When everything done, release the capture
    cap.release()
    vision.cv2.destroyAllWindows()
