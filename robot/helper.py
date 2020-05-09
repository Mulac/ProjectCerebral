from enum import Enum, auto


class Player(Enum):
    EMPTY = 0
    HUMAN = 1
    COMPUTER = 2


class Position:
    def __init__(self, pos, radius=None, player=None):
        self.pos = pos
        self.radius = radius
        self.player = player
        self.x = pos[0]
        self.y = pos[1]

    def translate_from_origin(self):
        x, y = 400 - self.x, 400 - self.y
        scale = 0.45
        return x*scale, y*scale
