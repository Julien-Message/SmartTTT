from random import random

from flask import Flask
from flask_sockets import Sockets
from game import Game, Result, Player

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/')
def game_socket(ws):
    game = None
    while not ws.closed:
        message = ws.receive()
        print(message)
        if game is None and message == "new":
            game = Game()
            print("New Game")
            player_is = Game.random_player()
            if player_is == Player.CIRCLE:
                _, _, result = playGame(game)
            ws.send(str(game.board))
        elif game is not None:
            try:
                move = int(message)
                print("moving", move)
                game.play(move)
                playGame(game)
                ws.send(str(game.board))
            except Exception:
                pass


def playGame(game):
    possible_moves = game.get_possible_moves()
    i = int(random() * len(possible_moves))
    step = possible_moves[i]
    player = game.currentPlayer
    return step, player, game.play(step[0], step[1])


@app.route('/')
def hello():
    print("begin")
    end = False
    game = Game()
    while not end:
        possible_moves = game.get_possible_moves()
        if len(possible_moves) == 0:
            print("Draw")
            end = True
        else:
            step, player, result = playGame(game)
            if result[0] == Result.NEXT_MOVE:
                print(player, step)
            elif result[0] == Result.WON:
                print(player, "played", step, "and won with line", result[1])
                end = True

    return ""


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    print("Serving Server on port 5000")
    try:
        server = pywsgi.WSGIServer(
            ('', 5000), app, handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("Keyboard Interruption...")
