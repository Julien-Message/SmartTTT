from game import Tile


def save(moves, player):
    with open('games.csv', 'a') as file:
        for move in moves:
            file.write(str(move))
        if player is Tile.CIRCLE:
            file.write("O")
        elif player is Tile.CROSS:
            file.write("X")
        else:
            file.write("N")
        file.write('\n')
        file.close()


def read():
    with open('games.csv', 'r') as file:
        content = file.readlines()
        content = [x.strip() for x in content]
        file.close()
        return content
