from .board import Board, Player
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

    def is_valid_move(self, brd):
        if self.stage == 1:
            return self.stage1Move(brd)
        elif self.stage == 2:
            return self.stage2Move(brd)
        elif self.stage == 3:
            return self.stage3Move(brd)
        else:
            raise Exception("Game in an invalid stage")

    def stage1Move(self, brd):
        diff_count = 0

        for ring in range(3):
            for row in range(3):
                for col in range(3):
                    if row == 1 and col == 1:   # This is important 
                        continue                # We never want to look at the center
                    vision = brd[ring][row][col]
                    model = self.board[ring][row][col]
                    if vision != model:
                        if diff_count > 0 or model != Player.EMPTY or vision != self.next_player():
                            return False
                        diff_count += 1
        
        return diff_count == 1

    def stage2Move(self, brd):
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
                        vNeighbours = self.getNeighbours(ring, row, col, brd)
                        mNeighbours = self.getNeighbours(ring, row, col, self.board)
                        if (move or
                            vNeighbours.count(player) != mNeighbours.count(player) + 1 or
                            vNeighbours.count(opponent) != mNeighbours.count(opponent)):
                            return False
                        move = ring, row, col

        if not move:
            return False
        
        # Was a mill created
        if self.isMill(brd, *move):
            return len(removes) == 1
        else:
            return changes == 2

    def isMill(self, board, i, j, k):
        if j == 1 and k == 1:
            raise Exception("Can't look at the center of the board")
        if board[i][j][k] == Player.EMPTY:
            return False
        elif (j == 0 or j == 2) and (k == 0 or k == 2):   # Corner case can't go accross levels
            return (len(set(board[i][:][k])) <= 1 or len(set(board[i][j][:])) <= 1)
        else:
            return (len(set(board[:][j][k])) <= 1 or
                    len(set(board[i][:][k])) <= 1 or
                    len(set(board[i][j][:])) <= 1)

    def getNeighbours(self, i, j, k, board):
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

    def build_board(self, isects):
        self.isects = [[[0 for z in range(3)] for y in range(3)] for x in range(3)]

        tempx = sorted(isects, key=lambda p: p.x)
        middle = tempx[9:15]
        del tempx[9:15]

        for x in range(0, 18, 3):   # Look down each column (except for center column and add isects)
            tempy = sorted(tempx[x:x + 3], key=lambda p: p.y)   # Order the column by its y position
            for i in range(3):  # Add to the correct position in the 3x3x3 array
                if x < 9:
                    col = 0
                    ring = x // 3
                else:
                    col = 2
                    ring = (x % 5) // 2

                self.isects[ring][i][col] = tempy[i]

        middle = sorted(middle, key=lambda p: p.y)
        self.isects[0][0][1] = middle[0]
        self.isects[1][0][1] = middle[1]
        self.isects[2][0][1] = middle[2]
        self.isects[2][2][1] = middle[3]
        self.isects[1][2][1] = middle[4]
        self.isects[0][2][1] = middle[5]

    def compute_state(self, counters):
        board = [[[Player.EMPTY for z in range(3)] for y in range(3)] for x in range(3)]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if j == 1 and k == 1:
                        continue
                    isect = self.isects[i][j][k]
                    for counter in counters:
                        if euclidean(counter[:2], isect.pos) < 15:
                            if counter[5] > 100:
                                board[i][j][k] = Player.HUMAN
                            else:
                                board[i][j][k] = Player.COMPUTER
                    
        return board

    def show(self):
        # print()
        # for ring in self.board:
        #     print(ring)
        b = self.board

        app = QApplication(sys.argv)
        win = QWidget()
        grid = QGridLayout()

        grid.addWidget(QLabel(b[0][0][0].name),0,0)
        grid.addWidget(QLabel(b[0][0][1].name),0,3)
        grid.addWidget(QLabel(b[0][0][2].name),0,6)
        grid.addWidget(QLabel(b[0][1][0].name),3,0)
        grid.addWidget(QLabel(b[0][1][2].name),3,6)
        grid.addWidget(QLabel(b[0][2][0].name),6,0)
        grid.addWidget(QLabel(b[0][2][1].name),6,3)
        grid.addWidget(QLabel(b[0][2][2].name),6,6)
        grid.addWidget(QLabel(b[1][0][0].name),1,1)
        grid.addWidget(QLabel(b[1][0][1].name),1,3)
        grid.addWidget(QLabel(b[1][0][2].name),1,5)
        grid.addWidget(QLabel(b[1][1][0].name),3,1)
        grid.addWidget(QLabel(b[1][1][2].name),3,5)
        grid.addWidget(QLabel(b[1][2][0].name),5,1)
        grid.addWidget(QLabel(b[1][2][1].name),5,3)
        grid.addWidget(QLabel(b[1][2][2].name),5,5)
        grid.addWidget(QLabel(b[2][0][0].name),2,2)
        grid.addWidget(QLabel(b[2][0][1].name),2,3)
        grid.addWidget(QLabel(b[2][0][2].name),2,4)
        grid.addWidget(QLabel(b[2][1][0].name),3,2)
        grid.addWidget(QLabel(b[2][1][2].name),3,4)
        grid.addWidget(QLabel(b[2][2][0].name),4,2)
        grid.addWidget(QLabel(b[2][2][1].name),4,3)
        grid.addWidget(QLabel(b[2][2][2].name),4,4)

        win.setLayout(grid)
        win.setWindowTitle("Nine Mens Morris Representation")
        win.setGeometry(50,50,450,450)
        win.show()
        sys.exit(app.exec_())
