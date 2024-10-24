from flask_socketio import Namespace, emit, ConnectionRefusedError, join_room, leave_room, send, rooms
from flask import request
from flask_login import current_user

from Game import Game
global gameRoom 
gameRoom = "gameRoom"

global players
players = []

global game

class Playing(Namespace):

    def on_connect(self):
        print(f"{request.sid} connected to game")
        join_room(gameRoom,request.sid)
        current_user.sid = request.sid
        players.append(current_user)
        print(rooms(request.sid))
        return "connected"

    def on_disconnect(self):
        print(f"{request.sid} disconnected from game")
        leave_room(gameRoom,request.sid)
        current_user.sid = None
        players.pop(current_user)
        return "ok"

    def on_start(self):
        print("starting game")
        return "ok"
    


class Home(Namespace):
    def on_connect(self):
        print("test")
        raise ConnectionRefusedError('unauthorized!')
    

class Admin(Namespace):
    def on_connect(self):
        print("admin connected")
        return "connected"
    
    def on_start_game(self):
        print("starting game")
        game = Game(players)
        emit("start", broadcast=True, namespace="/play")
        send("started", namespace="/admin")
        game.start()
        return "ok"
    