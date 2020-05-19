import math
import sys
import os


def reach(x, y):
    square = (210-x)**2 + (210-y)**2
    reach = math.sqrt(square)
    return reach


def upper(d):
    length = d / 3
    change = length - 75
    motor_conversion = 360 / (6 * math.pi)
    return change * motor_conversion


def lower(d):
    theta = math.acos(d/600)
    length = math.sqrt(17563 - 17556 * math.cos(theta + math.radians(12.5)))
    change = length - 128
    motor_conversion = 360 / (5 * math.pi)
    return change * motor_conversion


def base(x, y):
    angle = math.atan2((210-x), (210-y)) - math.pi / 4
    motor_conversion = 1100 / 0.726
    return angle * motor_conversion


def move_arm(x, y):
    d = reach(x, y)

    u = upper(d)
    l = lower(d)
    b = base(x, y)

    return int(u), int(l), int(b)


def make_tictactoe_move(move, counters):
    # for now we just want to move the arm to one location
    #u1, l1, b1 = 0, 0, 0
    # Move arm to next available counter
    free_counter = counters['spare'][0]
    u1, l1, b1 = move_arm(*free_counter.translate_from_origin())

    # Finds the position of empty move space
    x, y = counters[move].translate_from_origin()
    u2, l2, b2 = move_arm(x, y)

    os.system("ssh ev3 ./ev3control.py {} {} {} {} {} {}".format(u1, l1, b1, u2, l2, b2))


if __name__ == '__main__':
    assert len(sys.argv) == 4
    if sys.argv[3] == 'print':
        print("Motor Degrees")
        print("Upper: {}\nLower: {}\nBase: {}".format(*move_arm(int(sys.argv[1]), int(sys.argv[2]))))
    elif sys.argv[3] == 'move':
        os.system("ssh ev3 ./ev3control.py {} {} {} {} {} {}".format(0, 0, 0, *move_arm(int(sys.argv[1]), int(sys.argv[2]))))
    else:
        print("ERROR\nUsage: python3 control.py [x] [y] [print/move]")
