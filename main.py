import vision
from minimax import negamax
from boards.tttBoard import TicTacToe
from boards.nmmBoard import NineMensMorris

representation = TicTacToe()
representation.show()

cap = vision.cv2.VideoCapture(0)
frame_count = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_count += 1
    if frame_count % 1 == 0:
        if frame_count == 1:
            intersections = vision.find_board(frame, 4)
            representation.build_board(intersections)

        counters, cimg = vision.find_counters(frame)
        if counters is not None:    # Counters have started being placed
            board = representation.compute_state(counters)
            if representation.is_valid_move_state(board):
                representation.update_board(board)
                representation.show()

        # Display the resulting frame
        vision.cv2.imshow('counters', cimg)
    if vision.cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
vision.cv2.destroyAllWindows()