from random import random

from flask import Flask
from flask_sockets import Sockets

from game import Game, Result

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


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
            i = int(random() * len(possible_moves))
            step = possible_moves[i]
            player = game.currentPlayer
            result = game.play(step[0], step[1])
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
