from itertools import product
from .board import Board, Player
from vision import Position


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

    def build_board(self, get_isects, frame):
        isects = get_isects(frame, 4)
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

        # Return the corners of the board
        return [isects[0][0], isects[3][0], isects[0][3], isects[3][3]]

    def compute_state(self, counters):
        counter_positions = {}  # Hold all board positions / counter positions
        board = [[Player.EMPTY for x in range(3)] for y in range(3)]    # Our temporary board state

        for x in range(9):  # First calculate each board position and mark as empty
            row = x // 3
            col = x % 3
            center = 0.5 * (self.isects[row][col].pos + self.isects[row+1][col+1].pos)
            counter_positions[col, row] = Position(center, player=Player.EMPTY)

        for counter in counters:
            for x in range(9):
                row = x // 3
                col = x % 3         # Find counters that are on a board position
                if (self.isects[row][col].x < counter.x < self.isects[row + 1][col + 1].x and
                        self.isects[row + 1][col + 1].y > counter.y > self.isects[row][col].y):

                    board[col][row] = counter.player        # Update our temp board
                    counter_positions[col, row] = counter   # Mark board position with the counter
                    counters.remove(counter)                # Remove that counter as it has been found
                    break

        # The remaining counters are not on the board so will be marked as spare
        counter_positions['spare'] = [c for c in counters if c.player == Player.COMPUTER]

        # for x in range(9):
        #     row = x // 3
        #     col = x % 3
        #
        #     for c in counters:
        #         if (self.isects[row][col].x < c[0] < self.isects[row + 1][col + 1].x and
        #                 self.isects[row + 1][col + 1].y > c[1] > self.isects[row][col].y):
        #
        #             if c[5] > 80:
        #                 player = Player.HUMAN
        #                 board[col][row] = player
        #             else:
        #                 player = Player.COMPUTER
        #                 board[col][row] = player

        return board, counter_positions

    def show(self):
        print("\n\n")
        for row in self.board:
            print(row[0].name, row[1].name, row[2].name)
