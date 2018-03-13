import json
from random import random

from flask import Flask
from flask_sockets import Sockets
from game import Game, Result, Player

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/game')
def game_socket(ws):
    game = None
    while not ws.closed:
        message = ws.receive()
        print(message)
        if message == "new":
            game = Game()
            print("New Game")
            player_is = Game.random_player()
            if player_is == Player.CIRCLE:
                _, _, result = playGame(game)
            ws.send(generateMessage(Result.NON_PLAYABLE, game.board))
        elif game is not None:
            try:
                move = int(message)
                print("moving", move)
                result, lines = game.play(move)
                if result == Result.NEXT_MOVE:
                    playGame(game)
                ws.send(generateMessage(result, game.board))
            except Exception:
                pass


def generateMessage(result, board):
    array = [board[i].name.lower() for i in range(9)]
    return json.dumps({'result': result.name.lower(), 'board': array})


def playGame(game):
    possible_moves = game.get_possible_moves()
    i = int(random() * len(possible_moves))
    step = possible_moves[i]
    player = game.currentPlayer
    return step, player, game.play(step)


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
