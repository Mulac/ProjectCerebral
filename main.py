import vision
from boards.tttBoard import TicTacToe
from boards.nmmBoard import NineMensMorris

Representation = NineMensMorris()
Representation.show()

cap = vision.cv2.VideoCapture(0)
frame_count = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_count += 1
    if frame_count % 1 == 0:
        if frame_count == 1:
            intersections = vision.find_board(frame, 4)
            Representation.build_board(intersections)

        counters, cimg = vision.find_counters(frame)
        if counters is not None:    # Counters have started being placed
            board = Representation.compute_state(counters)
            if Representation.is_valid_move(board):
                Representation.update_board(board)
                Representation.show()

        # Display the resulting frame
        vision.cv2.imshow('counters', cimg)
    if vision.cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
vision.cv2.destroyAllWindows()