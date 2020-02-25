import cv2
import numpy as np
from poly_point_isect import isect_segments
from scipy.spatial.distance import pdist, euclidean, squareform
from tttBoard import *

def preprocess(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    height, width = img.shape[:2]
    center = width/2, height/2

    kernel_size = 13
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

    return blur_gray
    

def find_board(img):
    height, width = img.shape[:2]
    center = width/2, height/2

    low_threshold = 40
    high_threshold = 90
    edges = cv2.Canny(img, low_threshold, high_threshold)
    line_image = np.copy(frame) * 0 

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, np.array([]), 25, 30)

    line_segments = []
    r = 0
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                x3,y3 = x1+(x1-x2)*r, y1+(y1-y2)*r
                x4,y4 = x2+(x2-x1)*r, y2+(y2-y1)*r
                line_segments.append(((x3, y3), (x4, y4)))
                cv2.line(line_image,(int(x3),int(y3)),(int(x4),int(y4)),(255,0,0),3)

    line_image = cv2.addWeighted(frame, 0.8, line_image, 0.7, 0)

    isects = isect_segments(line_segments)
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

    class position():
        def __init__(self, pos):
            self.pos = pos
            self.ofset = euclidean(center, pos)
            self.x = pos[0]
            self.y = pos[1]

    positions = []
    for group in groups:
        points = [isects[i] for i in group]
        avg = np.mean(points, axis=0)
        positions.append(position(avg))

    # Get the closest 4 intersections to the center
    positions = sorted(positions, key=lambda p: p.ofset)
    positions = positions[:4]   
    # Order the intersections from top to bottom
    positions = sorted(positions, key=lambda p: p.x)
    positions[:2] = sorted(positions[:2], key=lambda p: p.y)
    positions[2:] = sorted(positions[2:], key=lambda p: p.y)
    for p in positions:
        x, y = p.pos
        cv2.circle(line_image, (int(x), int(y)), 2, (0, 255, 0), 4) 

    cv2.imshow('board',line_image)
    return positions


def find_counters(img):

    cimg = np.copy(frame)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,7,param1=35,param2=30,minRadius=15,maxRadius=25)
    if circles is not None:
        circles = np.uint16(np.around(circles))[0]
        for i in range(len(circles)):
            # draw the outer circle
            cv2.circle(cimg,(circles[i][0],circles[i][1]),circles[i][2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(circles[i][0],circles[i][1]),2,(0,0,255),3)
            # grab the colour of the circle 
            # circles[i].append()

    return circles, cimg


def compute_state(counters):
    board = [[Player.EMPTY for x in range(3)] for y in range(3)]
    
    for c in counters:
        if c[0] < intersections[0].x:
            col = 0
        elif c[0] < intersections[2].x:
            col = 1
        else:
            col = 2
        if c[1] < intersections[0].y:
            row = 0
        elif c[1] < intersections[1].y:
            row = 1
        else:
            row = 2

        if frame[c[1], c[0]][2] > 100:
            board[row][col] = Player.HUMAN
        else:
            board[row][col] = Player.COMPUTER
    
    return board


if __name__ == "__main__":
    global frame, intersections

    Representation = ttt()
    Representation.show()

    cap = cv2.VideoCapture(0)
    frame_count = 0

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_count += 1
        if (frame_count % 1 == 0):
            # Find the board position
            img = preprocess(frame)
            if frame_count == 1:
                intersections = find_board(img)

            
            counters, cimg = find_counters(img)
            if counters is not None:    # Counters have started being placed
                board = compute_state(counters)
                if Representation.isValidMove(board):
                    Representation.updateBoard(board)
                    Representation.show()
                

            # Display the resulting frame
            cv2.imshow('counters', cimg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    # img = cv2.imread('imgs/ttt_wc.jpg')
    # img = cv2.resize(img, (0,0), fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)

