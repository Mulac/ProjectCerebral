import numpy as np
from copy import copy
from itertools import product
from .board import Board, Player, Position
from robot.helper import BOARD, BOARD_SIZE


class TicTacToe(Board):

    def __init__(self):
        super(TicTacToe, self).__init__()
        self.board = [[Player.EMPTY for x in range(3)] for y in range(3)]

    def possible_moves(self):
        return [(x, y) for x, y in product(range(3), repeat=2) if self.board[x][y] == Player.EMPTY]

    def play_move(self, move):
        x, y = move
        if self.board[x][y] != Player.EMPTY:
            raise Exception("Player has already made that move")
        self.board[x][y] = self.player
        self.move += 1
        self.switch_player()

    def is_end(self):
        # Start by adding the diagonals
        lines = [[self.board[i][i] for i in range(3)], [self.board[i][2-i] for i in range(3)]]
        # Now Add the horizontals and verticals
        for i in range(3):
            lines.extend([[row[i] for row in self.board], self.board[i]])
        # Check if any line contains the same value, if so and not empty return the winner
        for line in lines:
            if len(set(line)) == 1 and line[0] != Player.EMPTY:
                return line[0]

        # Is a tie if no more possible moves
        if self.move >= 9:
            return Player.EMPTY

        return None

    def is_valid_move_state(self, brd):
        diff_count = 0

        for row in range(3):
            for col in range(3):
                current = self.board[row][col]
                vision = brd[row][col]
                if vision != current:  # Find the differences
                    # Make sure only 1 difference with the correct player choosing empty Position
                    if diff_count > 0 or current != Player.EMPTY or vision != self.player:
                        return False
                    diff_count += 1

        # Ensures a move has actually been made
        return diff_count == 1

    def build_board(self, frame, vision):
        isects = vision.find_board(frame, 4, r=0)

        if len(isects) != 4:
            return False, None

        frame, corners = vision.deskew(frame, isects, scale=1/3)
        for p in BOARD:
            vision.cv2.circle(frame, (int(p[0]), int(p[1])), 2, (0, 255, 0), 4)     

        vision.cv2.imshow('deskew', frame)
        
        a = BOARD_SIZE / 3 # size of the tictactoe spaces
        x, y = BOARD[0]

        self.isects = [ [Position((x, y)), Position((x+a, y)), Position((x+a+a, y)), Position((x+a+a+a, y))],
                        [Position((x, y+a)), Position((x+a, y+a)), Position((x+a+a, y+a)), Position((x+a+a+a, y+a))],
                        [Position((x, y+a+a)), Position((x+a, y+a+a)), Position((x+a+a, y+a+a)), Position((x+a+a+a, y+a+a))],
                        [Position((x, y+a+a+a)), Position((x+a, y+a+a+a)), Position((x+a+a, y+a+a+a)), Position((x+a+a+a, y+a+a+a))] ]
        
        # Convert all positions to numpy array
        for row in self.isects:
            for x in row:
                x.pos = np.array(x.pos)

        # Return the corners of the board
        return True, corners

    def compute_state(self, counters):
        counter_positions = {}  # Hold all board positions / counter positions
        board = [[Player.EMPTY for x in range(3)] for y in range(3)]    # Our temporary board state
        spare = copy(counters)  # Will remove as we find them on the board

        for x in range(9):  # First calculate each board position and mark as empty
            row = x // 3
            col = x % 3
            center = (self.isects[row][col].pos + self.isects[row+1][col+1].pos) / 2
            counter_positions[col, row] = Position(center, player=Player.EMPTY)

        for counter in counters:
            for x in range(9):
                row = x // 3
                col = x % 3         # Find counters that are on a board position
                if (self.isects[row][col].x < counter.x < self.isects[row + 1][col + 1].x and
                        self.isects[row + 1][col + 1].y > counter.y > self.isects[row][col].y):

                    board[col][row] = counter.player        # Update our temp board
                    counter_positions[col, row] = counter   # Mark board position with the counter
                    spare.remove(counter)                # Remove that counter as it has been found
                    break

        # The remaining counters are not on the board so will be marked as spare
        counter_positions['spare'] = [c for c in spare if c.player == Player.COMPUTER]

        return board, counter_positions

    def show(self):
        print("\n\n")
        for row in self.board:
            print(row[0].name, row[1].name, row[2].name)
