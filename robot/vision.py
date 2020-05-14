import cv2
import numpy as np
from robot.helper import Player, Position, WINDOW_SIZE, BOARD_SIZE, BOARD
from poly_point_isect import isect_segments
from scipy.spatial.distance import pdist, euclidean, squareform

center = None


def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel_size = 9
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    return blur_gray


def deskew(img, pts1, scale=1):
    board_size = BOARD_SIZE * scale # This allows for skewing with only the center of the tictactoe board
    margin = (WINDOW_SIZE - board_size) / 2

    pts2 = np.float32([[margin, margin], [board_size+margin, margin], [margin, board_size+margin], [board_size+margin, board_size+margin]])

    transformation = cv2.getPerspectiveTransform(pts1, pts2)
    inverse = cv2.getPerspectiveTransform(pts2, pts1)
    board = np.float32([BOARD])
    corners = cv2.perspectiveTransform(board, inverse)

    return cv2.warpPerspective(img, transformation, (WINDOW_SIZE, WINDOW_SIZE)), np.float32(corners).reshape(4, 2) 
    

def find_board(img, limit, r=0.17, debug=True):
    global center
    frame = np.copy(img)
    line_image = np.copy(frame) * 0 
    img = preprocess(img)

    height, width = img.shape[:2]
    center = width/2, height/2

    low_threshold = 35
    high_threshold = 90
    edges = cv2.Canny(img, low_threshold, high_threshold)
    cv2.imshow('canny', edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, np.array([]), 50, 24)

    line_segments = []
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                x3, y3 = x1+(x1-x2)*r, y1+(y1-y2)*r
                x4, y4 = x2+(x2-x1)*r, y2+(y2-y1)*r
                line_segments.append(((x3, y3), (x4, y4)))
                cv2.line(line_image, (int(x3), int(y3)), (int(x4), int(y4)), (255, 0, 0), 3)

    line_image = cv2.addWeighted(frame, 0.8, line_image, 0.7, 0)

    isects = np.array(isect_segments(line_segments))
    distances = squareform(pdist(isects, 'euclidean'))

    # Use the distances matrix to group agreeing intersections together 
    # -> agreeing intersections are within 20px of each other
    # -> the groups are stored by their index in the 'isects' list

    tol = 20
    visited = []
    groups = []
    for i in range(len(isects)):
        if i not in visited:
            neighbours = []
            for j in range(len(isects)):
                if distances[i][j] < tol:
                    neighbours.append(j)
                    visited.append(j)
            groups.append(neighbours)

    positions = []
    for group in groups:
        points = [isects[i] for i in group]
        avg = np.mean(points, axis=0)
        positions.append(Position(avg))

    # Get the closest 4 intersections to the center
    positions = sorted(positions, key=lambda p: euclidean(center, p.pos))
    positions = positions[:limit]   
    print("number isects found:", len(positions))

    for p in positions:
        cv2.circle(line_image, (int(p.x), int(p.y)), 2, (0, 255, 0), 4) 
    
    if debug:
        cv2.imshow('{},{}'.format(height, width), line_image)
    return np.float32([p.pos for p in positions])


def find_counters(frame, size=BOARD_SIZE//6, variance=8):

    cimg = np.copy(frame)
    img = preprocess(frame)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 7, param1=35, param2=30, minRadius=size-variance, maxRadius=size+variance)
    counters = []
    
    if circles is not None:
        circles = np.uint16(np.around(circles[0]))

        for i in range(len(circles)):
            # Grab the colour at the center of the circle
            col = frame[circles[i][1], circles[i][0]]
            red = col[2]
            if red > 40:
                player = Player.HUMAN
                cv2.circle(cimg, (circles[i][0], circles[i][1]), circles[i][2], (0, 255, 0), 2)
                cv2.circle(cimg, (circles[i][0], circles[i][1]), 2, (255, 0, 0), 3)
            else:
                player = Player.COMPUTER
                cv2.circle(cimg, (circles[i][0], circles[i][1]), circles[i][2], (0, 255, 0), 2)
                cv2.circle(cimg, (circles[i][0], circles[i][1]), 2, (0, 0, 255), 3)

            counters.append(Position((circles[i][0], circles[i][1]), radius=circles[i][2], player=player))

        return counters, cimg
    return None, cimg
