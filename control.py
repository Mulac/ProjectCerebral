import math
import os


def dist_from_pivot(x, y):
    square = (21-x)**2 + (21-y)**2
    return math.sqrt(square)


def upper(d):
    return d / 3


def lower(d):
    theta = math.acos(d/60)
    return math.sqrt(153 + 67.88225099 * math.cos(theta+40/75))


def base_angle(x, y):
    return math.atan2((21-x), (21-y))


def move_arm(x, y):
    d = dist_from_pivot(x, y)

    u = upper(d)
    l = lower(d)
    b = base_angle(x, y)

    return u, l, b


# TODO: This will only work for a tictactoe move
def make_tictactoe_move(move, counters):
    # Move arm to next available counter
    free_counter = counters['spare'][0]
    u1, l1, b1 = move_arm(*free_counter.translate_from_origin())

    # Finds the position of empty move space
    position = counters[move].translate_from_origin()
    u2, l2, b2 = move_arm(*position)

    os.system("ssh ev3 ./ev3control {} {} {} {} {} {}".format(u1, l1, b1, u2, l2, b2))
