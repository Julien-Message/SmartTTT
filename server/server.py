import json
import threading
from time import sleep

from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from numpy.random import choice

import file
import neural
from game import Game, Result, Tile

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/game')
def game_socket(ws):
    game = None
    while not ws.closed:
        message = ws.receive()
        if message == "new":
            game = Game()
            player_is = Game.random_player()
            print("New Game", player_is)
            if player_is == Tile.CIRCLE:
                result, _ = play_game(game)
            else:
                result = Result.NEXT_MOVE
            ws.send(generate_message(result, game.board))
        elif game and message:
            move = int(message)
            print("You play", move)
            result, lines = game.play(move)
            if result == Result.NEXT_MOVE:
                result, lines = play_game(game)
            elif result == Result.WON:
                print("finished")
                file.save(game.moves, game.currentPlayer)
            elif len(game.moves) == 9:
                print("finished")
                file.save(game.moves, None)

            ws.send(generate_message(result, game.board))


def generate_message(result, board):
    array = [board[i].name.lower() for i in range(9)]
    return json.dumps({'result': result.name.lower(), 'board': array})


def play_game(game):
    possible_moves = game.get_possible_moves()
    neural_moves = neural.play(game)
    neural_moves = [v for (i, v) in enumerate(neural_moves) if i in possible_moves]
    neural_moves /= sum(neural_moves)
    i = choice(possible_moves, 1, p=neural_moves)[0]
    print("computer plays", i)
    return game.play(i)


def nn_thread():
    while True:
        neural.update_nn()
        sleep(60)


if __name__ == "__main__":
    try:
        nn = threading.Thread(target=nn_thread)
        nn.start()
        server = pywsgi.WSGIServer(
            ('', 5000), app, handler_class=WebSocketHandler)
        print("Serving Server on port 5000")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Keyboard Interruption...")
