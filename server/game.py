from enum import Enum
from random import random


class Tile(Enum):
    BLANK = 0
    CROSS = 1
    CIRCLE = 2


class Player(Enum):
    CROSS = 1
    CIRCLE = 2


class Result(Enum):
    NON_PLAYABLE = 0
    NEXT_MOVE = 1
    DRAW = 2
    WON = 3


class Game:
    def __init__(self) -> None:
        self.board = [Tile.BLANK, Tile.BLANK, Tile.BLANK,
                      Tile.BLANK, Tile.BLANK, Tile.BLANK,
                      Tile.BLANK, Tile.BLANK, Tile.BLANK]
        self.currentPlayer = Player.CROSS
        self.possible_moves = [i for i in range(9)]
        self.moves = []

    def play(self, x):

        if self.board[x] != Tile.BLANK:
            return Result.NON_PLAYABLE, []

        self.board[x] = self.currentPlayer
        self.possible_moves.remove(x)
        self.moves += [x]

        result = self.has_won(x)

        if len(result) > 0:
            return Result.WON, result
        else:
            if self.currentPlayer == Player.CROSS:
                self.currentPlayer = Player.CIRCLE
            else:
                self.currentPlayer = Player.CROSS
            return Result.NEXT_MOVE, []

    diagonal1 = [0, 4, 8]
    diagonal2 = [2, 4, 6]

    def has_won(self, x):
        x_line = [x - (x % 3) + i for i in range(3)]
        x_column = [x % 3 + 3 * i for i in range(3)]

        player_line = [self.currentPlayer,
                       self.currentPlayer,
                       self.currentPlayer]

        winning_lines = []

        if x in Game.diagonal1 and [self.board[i] for i in Game.diagonal1] == player_line:
            winning_lines.append(Game.diagonal1)

        if x in Game.diagonal2 and [self.board[i] for i in Game.diagonal2] == player_line:
            winning_lines.append(Game.diagonal2)

        if [self.board[i] for i in x_line] == player_line:
            winning_lines.append(x_line)

        if [self.board[i] for i in x_column] == player_line:
            winning_lines.append(x_column)

        return winning_lines

    def get_possible_moves(self):
        return self.possible_moves

    @staticmethod
    def random_player():
        i = int(random() * 2 + 1)
        if i == 1:
            return Player.CROSS
        else:
            return Player.CIRCLE
