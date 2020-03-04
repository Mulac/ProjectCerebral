from .board import Board, Player
from vision import Position


class TicTacToe(Board):

    def __init__(self):
        super(TicTacToe, self).__init__()
        self.board = [[Player.EMPTY for x in range(3)] for y in range(3)]

    def isValidMove(self, brd):
        diff_count = 0

        for row in range(3):
            for col in range(3):
                current = self.board[row][col]
                vision = brd[row][col]
                if vision != current:  # Find the differences
                    # Make sure only 1 difference with the correct player choosing empty Position
                    if diff_count > 0 or current != Player.EMPTY or vision != self.nextPlayer():
                        return False
                    diff_count += 1

        # Ensures a move has actually been made
        return diff_count == 1

    def build_board(self, isects):
        # Order intersections from top to bottom
        isects = sorted(isects, key=lambda p: p.x)
        isects[:2] = sorted(isects[:2], key=lambda p: p.y)
        isects[2:] = sorted(isects[2:], key=lambda p: p.y)
        # Extrapolate intersections to get the whole playing area
        isects = [isects[:2], isects[2:]]
        for i in range(2):
            isects[i].insert(0, Position(2 * isects[i][0].pos - isects[i][1].pos))
            isects[i].append(Position(2 * isects[i][-1].pos - isects[i][-2].pos))
        isects.insert(0, list.copy(isects[0]))
        isects.append(list.copy(isects[-1]))
        for j in range(4):
            isects[0][j] = Position([2 * isects[0][j].x - isects[2][j].x, isects[0][j].y])
            isects[-1][j] = Position([2 * isects[-1][j].x - isects[-3][j].x, isects[-1][j].y])

        self.isects = isects

    def compute_state(self, counters):
        # Begin to build board representation
        board = [[Player.EMPTY for x in range(3)] for y in range(3)]

        for x in range(9):
            row = x // 3
            col = x % 3

            for c in counters:
                if (self.isects[row][col].x < c[0] < self.isects[row + 1][col + 1].x and
                        self.isects[row + 1][col + 1].y > c[1] > self.isects[row][col].y):

                    if c[5] > 100:
                        board[col][row] = Player.HUMAN
                    else:
                        board[col][row] = Player.COMPUTER

        return board

    def show(self):
        print("\n\n")
        for row in self.board:
            print(row[0].name, row[1].name, row[2].name)
