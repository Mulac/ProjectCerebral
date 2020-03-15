from .board import Board, Player
from vision import Position
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from scipy.spatial.distance import pdist, euclidean


class NineMensMorris(Board):

    def __init__(self):
        super(NineMensMorris, self).__init__()
        self.board = [[[Player.EMPTY for z in range(3)] for y in range(3)] for x in range(3)]
        self.stage = 1

    @staticmethod
    def is_mill(board, i, j, k):
        if j == 1 and k == 1:
            raise Exception("Can't look at the center of the board")
        if board[i][j][k] == Player.EMPTY:
            return False
        elif (j == 0 or j == 2) and (k == 0 or k == 2):   # Corner case can't go across levels
            return len(set(board[i][:][k])) <= 1 or len(set(board[i][j][:])) <= 1
        else:
            return (len(set(board[:][j][k])) <= 1 or
                    len(set(board[i][:][k])) <= 1 or
                    len(set(board[i][j][:])) <= 1)

    @staticmethod
    def get_neighbours(i, j, k, board):
        if j == 1 and k == 1:
            raise Exception("Can't look at the center of the board")
        if (j == 0 or j == 2) and (k == 0 or k == 2):   # Corner positions with only 2 neighbours
            neighbours = [(i, j-1 if j == 2 else j+1, k), (i, j, k-1 if k == 2 else k+1)]
        elif i == 1:                                    # Middle ring with 4 neighbours
            neighbours = [(i, 0, k), (i, 2, k)] if j == 1 else [(i, j, 0), (i, j, 2)]
            neighbours.extend([(0, j, k), (2, j, k)])
        else:                                           # Remaining edge neighbours with 3 neighbours
            neighbours = [(i, 0, k), (i, 2, k)] if j == 1 else [(i, j, 0), (i, j, 2)]
            neighbours.append((1, j, k))
        return [board[x][y][z] for x, y, z in neighbours]

    def is_valid_move_state(self, brd):
        if self.stage == 1:
            return self.stage_1(brd)
        elif self.stage == 2:
            return self.stage_2(brd)
        else:
            raise Exception("Game in an invalid stage")

    def stage_1(self, brd):
        human_count = 0
        computer_count = 0

        diff_count = 0

        for ring in range(3):
            for row in range(3):
                for col in range(3):
                    if row == 1 and col == 1:   # This is important 
                        continue                # We never want to look at the center
                    vision = brd[ring][row][col]
                    model = self.board[ring][row][col]

                    # Update player counts
                    if model == Player.HUMAN:
                        human_count += 1
                    elif model == Player.COMPUTER:
                        computer_count += 1

                    # Check for valid differences (next player adds a piece to empty position)
                    if vision != model:
                        if diff_count > 0 or model != Player.EMPTY or vision != self.player:
                            return False
                        diff_count += 1

        # It's the next stage!
        if human_count and computer_count == 9:
            self.stage = 1
            return self.stage_2(brd)
        
        return diff_count == 1      # If there's only one difference accept the move

    def stage_2(self, brd):
        player = self.next_player()
        if player == Player.HUMAN:
            opponent = Player.COMPUTER
        else:
            opponent = Player.HUMAN

        # Find where the player has moved
        #   EXIT if not valid
        #   EXIT if not found
        # Check if player created a mill
        #   no?
        #       Ensure only one difference on board is made
        #   yes?
        #       Ensure exact one opponent piece is now missing
        move = ()
        changes = 0
        removes = []
        for ring in range(3):
            for row in range(3):
                for col in range(3):
                    if row == 1 and col == 1:   # This is important 
                        continue                # We never want to look at the center
                    
                    vision = brd[ring][row][col]
                    model = self.board[ring][row][col]

                    if vision != model:
                        changes += 1

                    if vision == Player.EMPTY and model == opponent:
                        removes.append((ring, row, col))
                    elif vision == player and model == Player.EMPTY:
                        vNeighbours = self.get_neighbours(ring, row, col, brd)
                        mNeighbours = self.get_neighbours(ring, row, col, self.board)
                        if (move or
                            vNeighbours.count(player) != mNeighbours.count(player) + 1 or
                            vNeighbours.count(opponent) != mNeighbours.count(opponent)):
                            return False
                        move = ring, row, col

        if not move:
            return False
        
        # Was a mill created
        if NineMensMorris.is_mill(brd, *move):
            return len(removes) == 1
        else:
            return changes == 2

    def is_end(self):
        if self.stage != 2:
            return None

        human_count = 0
        computer_count = 0
        for ring in range(3):
            for row in range(3):
                for col in range(3):
                    if row == 1 and col == 1:  # This is important
                        continue
                    if self.board == Player.HUMAN:
                        human_count += 1
                    elif self.board == Player.COMPUTER:
                        computer_count += 1

        if human_count <= 2:
            return Player.COMPUTER
        elif computer_count <= 2:
            return Player.HUMAN
        else:
            return None

    def play_move(self, move):
        raise NotImplementedError

    def build_board(self, get_isects, frame):
        # The intersections of the board are first ordered so that when computing the board state
        # counters that are over an intersection will be at the same index in the board data structure.

        # That is: a 3x3x3 array indexed first by ring level then row then col --> board[ring][row][col]

        # We then use the outer 4 intersections to translate the pixel measure to millimeters knowing the size
        # of our Nine Men's Morris board

        isects = get_isects(frame, 24)  # First grab the first 24 intersections from the center of the frame
        if len(isects) != 24:
            raise Exception("Could not find 24 intersections.  Found {}".format(len(isects)))
        self.isects = [[[Position((0, 0)) for z in range(3)] for y in range(3)] for x in range(3)]

        temp_x = sorted(isects, key=lambda p: p.x)
        middle = temp_x[9:15]
        del temp_x[9:15]

        for x in range(0, 18, 3):   # Look down each column (except for center column and add isects)
            temp_y = sorted(temp_x[x:x + 3], key=lambda p: p.y)   # Order the column by its y position
            for i in range(3):  # Add to the correct position in the 3x3x3 array
                if x < 9:
                    col = 0
                    ring = x // 3
                else:
                    col = 2
                    ring = (x % 5) // 2

                self.isects[ring][i][col] = temp_y[i]

        middle = sorted(middle, key=lambda p: p.y)  # Add the middle column
        self.isects[0][0][1] = middle[0]
        self.isects[1][0][1] = middle[1]
        self.isects[2][0][1] = middle[2]
        self.isects[2][2][1] = middle[3]
        self.isects[1][2][1] = middle[4]
        self.isects[0][2][1] = middle[5]

        # Return the 4 corners for image skewing and pixel -> millimeter translation
        return [self.isects[0][0][0], self.isects[0][0][2], self.isects[0][2][0], self.isects[0][2][2]]

    def compute_state(self, counters):
        counter_positions = {}
        board = [[[Player.EMPTY for z in range(3)] for y in range(3)] for x in range(3)]

        for counter in counters:
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        if j == 1 and k == 1:
                            continue
                        isect = self.isects[i][j][k]
                        if euclidean(counter.pos, isect.pos) < 15:
                            board[i][j][k] = counter.player
                            counter_positions[i, j, k] = counter
                            counters.remove(counter)
                        else:
                            counter_positions[i, j, k] = Position(self.isects[i][j][k].pos, player=Player.EMPTY)

        counter_positions['spare'] = [c for c in counters if c.player == Player.COMPUTER]

        # for i in range(3):
        #     for j in range(3):
        #         for k in range(3):
        #             if j == 1 and k == 1:
        #                 continue
        #             isect = self.isects[i][j][k]
        #             for counter in counters:
        #                 if euclidean(counter[:2], isect.pos) < 15:
        #                     if counter[5] > 40:
        #                         board[i][j][k] = Player.HUMAN
        #                     else:
        #                         board[i][j][k] = Player.COMPUTER
                    
        return board, counter_positions

    def show(self):
        print()
        for ring in self.board:
            print(ring)
        # b = self.board
        #
        # app = QApplication(sys.argv)
        # win = QWidget()
        # grid = QGridLayout()
        #
        # grid.addWidget(QLabel(b[0][0][0].name),0,0)
        # grid.addWidget(QLabel(b[0][0][1].name),0,3)
        # grid.addWidget(QLabel(b[0][0][2].name),0,6)
        # grid.addWidget(QLabel(b[0][1][0].name),3,0)
        # grid.addWidget(QLabel(b[0][1][2].name),3,6)
        # grid.addWidget(QLabel(b[0][2][0].name),6,0)
        # grid.addWidget(QLabel(b[0][2][1].name),6,3)
        # grid.addWidget(QLabel(b[0][2][2].name),6,6)
        # grid.addWidget(QLabel(b[1][0][0].name),1,1)
        # grid.addWidget(QLabel(b[1][0][1].name),1,3)
        # grid.addWidget(QLabel(b[1][0][2].name),1,5)
        # grid.addWidget(QLabel(b[1][1][0].name),3,1)
        # grid.addWidget(QLabel(b[1][1][2].name),3,5)
        # grid.addWidget(QLabel(b[1][2][0].name),5,1)
        # grid.addWidget(QLabel(b[1][2][1].name),5,3)
        # grid.addWidget(QLabel(b[1][2][2].name),5,5)
        # grid.addWidget(QLabel(b[2][0][0].name),2,2)
        # grid.addWidget(QLabel(b[2][0][1].name),2,3)
        # grid.addWidget(QLabel(b[2][0][2].name),2,4)
        # grid.addWidget(QLabel(b[2][1][0].name),3,2)
        # grid.addWidget(QLabel(b[2][1][2].name),3,4)
        # grid.addWidget(QLabel(b[2][2][0].name),4,2)
        # grid.addWidget(QLabel(b[2][2][1].name),4,3)
        # grid.addWidget(QLabel(b[2][2][2].name),4,4)
        #
        # win.setLayout(grid)
        # win.setWindowTitle("Nine Mens Morris Representation")
        # win.setGeometry(50,50,450,450)
        # win.show()
        # sys.exit(app.exec_())
