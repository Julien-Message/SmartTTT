import file
import numpy as np

from game import Tile

syn0 = 2 * np.random.random((18, 9)) - 1


def play(game):
    game_board = [1 if tile is Tile.CROSS else 0 for tile in game.board] \
                 + [1 if tile is Tile.CIRCLE else 0 for tile in game.board]
    x = np.array(game_board)
    global syn0
    y = nonlin(np.dot(x, syn0))
    print(y)
    return y


# sigmoid function
def nonlin(x, deriv=False):
    if deriv:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


def update_nn():
    games = file.read()
    boards = []
    outputs = []
    for game in games:
        winner = game[-1]
        winner_turn = 1 if winner != "N" else 0.5
        game = game[:-1]
        while game:
            next_move = int(game[-1])
            game = game[:-1]

            board = [0] * 18
            for index, move in enumerate(game):
                board[(index % 2) * 9 + int(move)] = 1

            output = [0] * 9
            output[next_move] = 1 - winner_turn

            boards.append(board)
            outputs.append(output)

            winner_turn = - winner_turn

    X = np.array(boards)
    Y = np.array(outputs)

    # initialize weights randomly with mean 0
    np.random.seed(4)
    global syn0
    syn0 = 2 * np.random.random((18, 9)) - 1
    l1 = None

    for i in range(20000):
        # forward propagation
        l0 = X
        l1 = nonlin(np.dot(l0, syn0))

        # how much did we miss?
        l1_error = Y - l1

        # multiply how much we missed by the
        # slope of the sigmoid at the values in l1
        l1_delta = l1_error * nonlin(l1, True)

        # update weights
        syn0 += np.dot(l0.T, l1_delta)

    print(l1)
    print("updated")
