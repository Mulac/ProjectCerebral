import cv2
import numpy as np
from poly_point_isect import isect_segments
from scipy.spatial.distance import pdist, euclidean, squareform

center = None

class Position():
    def __init__(self, pos):
        self.pos = pos
        self.ofset = euclidean(center, pos)
        self.x = pos[0]
        self.y = pos[1]


def preprocess(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    kernel_size = 13
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

    return blur_gray
    

def find_board(img, limit):
    global center
    frame = np.copy(img)
    line_image = np.copy(frame) * 0 
    img = preprocess(img)

    height, width = img.shape[:2]
    center = width/2, height/2

    low_threshold = 40
    high_threshold = 90
    edges = cv2.Canny(img, low_threshold, high_threshold)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, np.array([]), 25, 30)

    line_segments = []
    r = 0.12
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

    positions = []
    for group in groups:
        points = [isects[i] for i in group]
        avg = np.mean(points, axis=0)
        positions.append(Position(avg))

    # Get the closest 4 intersections to the center
    positions = sorted(positions, key=lambda p: p.ofset)
    positions = positions[:limit]   

    for p in positions:
        cv2.circle(line_image, (int(p.x), int(p.y)), 2, (0, 255, 0), 4) 

    cv2.imshow('board',line_image)
    return positions


def find_counters(frame):

    cimg = np.copy(frame)
    img = preprocess(frame)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,7,param1=35,param2=30,minRadius=15,maxRadius=37)
    
    if circles is not None:
        circles = np.uint16(np.around(circles[0]))
        colours = np.empty([len(circles), 3], dtype=int)
        for i in range(len(circles)):
            col = frame[circles[i][1], circles[i][0]]
            # grab the colour of the circle 
            colours[i][0] = int(col[0])
            colours[i][1] = int(col[1])
            colours[i][2] = int(col[2])
            # draw the outer circle
            cv2.circle(cimg,(circles[i][0],circles[i][1]),circles[i][2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(circles[i][0],circles[i][1]),2,(0,0,255),3)

        counters = np.concatenate((circles, colours), axis=1)
        return counters, cimg
    
    return None, cimg
