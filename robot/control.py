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
    change = length - 123
    motor_conversion = 360 / (5 * math.pi)
    return change * motor_conversion


def base(x, y):
    angle = math.atan2((210-x), (210-y)) - math.pi / 4
    motor_conversion = 1100 / 0.726
    return angle * motor_conversion + 450 # home position is off center


def move_arm(x, y):
    d = reach(x, y)

    u = upper(d)
    l = lower(d)
    b = base(x, y)

    return int(u), int(l), int(b)


def make_tictactoe_move(move, counters):
    # Find free counters to use
    free_counters = counters['spare']
    # Move arm to the counter to pick up
    u1, l1, b1 = move_arm(*free_counters[0].translate_from_origin())

    # Finds the position of move space
    x, y = counters[move].translate_from_origin()
    u2, l2, b2 = move_arm(x, y)

    os.system("ssh ev3 ./ev3control.py {} {} {} {} {} {}".format(u1, l1, b1, u2, l2, b2))


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'setup':
        d = 400
        os.system("ssh ev3 ./ev3control.py {} {} {} {} {} {}".format(0, 0, 0, int(upper(d)), int(lower(d)), int(base(0, 0))))
        d = 250
        os.system("ssh ev3 ./ev3control.py {} {} {} {} {} {}".format(0, 0, 0, int(upper(d)), int(lower(d)), int(base(0, 0))))
    elif len(sys.argv) == 4 and sys.argv[3] == 'print':
        print("Motor Degrees")
        print("Upper: {}\nLower: {}\nBase: {}".format(*move_arm(int(sys.argv[1]), int(sys.argv[2]))))
    elif len(sys.argv) == 4 and sys.argv[3] == 'move':
        os.system("ssh ev3 ./ev3control.py {} {} {} {} {} {}".format(0, 0, 0, *move_arm(int(sys.argv[1]), int(sys.argv[2]))))
    else:
        print("ERROR\nUsage: python3 control.py [x] [y] [print/move]\nOR python3 control.py setup")
