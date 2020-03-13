import math
import os


def dist_from_pivot(x, y):
    square = (21-x)**2 + (21-y)**2
    return math.sqrt(square)


def upper(d):
    return d / 3


def lower(d):
    theta = math.acos(d/60)

    # Sqrt (9^2 + t^2) + 8t cos(theta+0)
    return math.sqrt(153 + 67.88225099 * math.cos(theta+40/75))


def base_angle(x, y):
    return math.atan2((21-x), (21-y))


def move_arm(x, y):
    d = dist_from_pivot(x, y)

    u = upper(d)
    l = lower(d)
    b = base_angle(x, y)

    return u, l, b


def make_move(move, counters):
    # TODO:
    # Find avaliable counter
    # Get x&y of counter from origin
    u1, l1, b1 = move_arm(x1, y1)

    # TODO:
    # Find x&y of move from origin
    u2, l2, b2 = move_arm(x2, y2)

    os.system("ssh ev3 ./ev3control {} {} {} {} {} {}".format(u1, l1, b1, u2, l2, b2))
