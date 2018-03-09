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
        i = int(random() * 9)
        player = game.currentPlayer
        result = game.play(i)
        if result[0] == Result.NEXT_MOVE:
            print(player, i)
        elif result[0] == Result.WON:
            print(player, "played", i, "and won with line", result)
            end = True
        elif result[0] == Result.NON_PLAYABLE:
            pass
        else:
            print("Draw")
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
