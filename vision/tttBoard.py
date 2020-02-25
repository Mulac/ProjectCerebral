from enum import Enum, auto

class Player(Enum):
    EMPTY = auto()
    HUMAN = auto()
    COMPUTER = auto()


class ttt():

    def __init__(self):
        self.board = [[Player.EMPTY for x in range(3)] for y in range(3)]
        self.move = 0

    def isValidMove(self, brd):
        diff_count = 0

        for row in range(3):
            for col in range(3):
                current = self.board[row][col]
                vision = brd[row][col]
                if vision != current:   # Find the differences
                    # Make sure only 1 difference with the correct player choosing empty position
                    if diff_count > 0 or current != Player.EMPTY or vision != Player(self.nextPlayer()):
                        return False
                    diff_count += 1
        
        # Ensures a move has actually been made
        return diff_count == 1

    def nextPlayer(self):
        return self.move % 2 + 2

    def updateBoard(self, brd):
        self.board = brd
        self.move += 1

    def show(self):
        print("\n\n")
        for row in self.board:
            print(row[0].name, row[1].name, row[2].name)
