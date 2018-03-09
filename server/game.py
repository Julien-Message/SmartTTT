from enum import Enum


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
    WON = 2


class Game:
    def __init__(self) -> None:
        self.board = [[Tile.BLANK, Tile.BLANK, Tile.BLANK],
                      [Tile.BLANK, Tile.BLANK, Tile.BLANK],
                      [Tile.BLANK, Tile.BLANK, Tile.BLANK]]
        self.currentPlayer = Player.CROSS

    def play(self, x, y):
        if y is None:
            x, y = x % 3, x / 3

        if self.board[x][y] != Tile.BLANK:
            return Result.NON_PLAYABLE, []

        self.board[x][y] = self.currentPlayer

        result = self.has_won(x, y)

        if len(result) > 0:
            return Result.WON, result
        else:
            self.currentPlayer = 3 - self.currentPlayer  # 2 => 1; 1 => 2
            return Result.NEXT_MOVE, []

    def has_won(self, x, y):
        winning_lines = []
        if x == y and [self.board[0][0],
                       self.board[1][1],
                       self.board[2][2]] == [self.currentPlayer,
                                             self.currentPlayer,
                                             self.currentPlayer]:
            winning_lines.append([(0, 0), (1, 1), (2, 2)])

        if x + y == 2 and [self.board[0][2],
                           self.board[1][1],
                           self.board[2][0]] == [self.currentPlayer,
                                                 self.currentPlayer,
                                                 self.currentPlayer]:
            winning_lines.append([(0, 2), (1, 1), (2, 0)])

        if [self.board[x][0],
            self.board[x][1],
            self.board[x][2]] == [self.currentPlayer,
                                  self.currentPlayer,
                                  self.currentPlayer]:
            winning_lines.append([(x, 0), (x, 1), (x, 2)])

        if [self.board[0][y],
            self.board[1][y],
            self.board[2][y]] == [self.currentPlayer,
                                  self.currentPlayer,
                                  self.currentPlayer]:
            winning_lines.append([(0, y), (1, y), (2, y)])

        return winning_lines
