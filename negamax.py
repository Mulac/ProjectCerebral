from copy import deepcopy
from boards.board import Player

infinity = float('infinity')


def decision(game, depth):
    root_state = deepcopy(game)
    return negamax(root_state, depth)[0]


def evaluate(player, winner):
    if winner == player:
        return 100
    elif winner == Player.EMPTY:
        return 0
    else:
        return -100


def negamax(game, depth):

    best = [None, -infinity]

    winner = game.is_end()

    if depth == 0 or winner:
        score = evaluate(game.player, winner)
        return [None, score]

    state = game

    for move in game.possible_moves():
        game = deepcopy(state)

        game.play_move(move)

        value = negamax(game, depth - 1)
        value[0] = move
        value[1] *= -1

        if value[1] > best[1]:
            best = value

    return best
