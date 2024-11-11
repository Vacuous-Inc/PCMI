from flask_socketio import Namespace, emit, join_room, leave_room, send, rooms, ConnectionRefusedError
from flask import request
from flask_login import current_user

from User import User
from Game import Game
global gameRoom 
gameRoom = "gameRoom"

global players
players = []

global game

class Playing(Namespace):

    def on_connect(self):
        print(f"{current_user.name} at {request.sid} connected to game")
        if len(players) < 4:
            join_room(gameRoom,request.sid)
            tempUser = User.get(current_user.id)
            tempUser.sid = request.sid
            players.append(tempUser)
        print(rooms(request.sid))
        emit("connected", tempUser.info(), to=request.sid, namespace="/play")

    def on_disconnect(self):
        print(f"{request.sid} disconnected from game")
        leave_room(gameRoom,request.sid)
        current_user.sid = None
        players.pop(players.index(current_user))
        return "ok"

    def on_start(self):
        print("starting game")
        return "ok" 
    
    def send_game_data(self, message):
        emit("game_event", message, namespace="/play", to=gameRoom)

    def on_hit(self, message):
        data = dict(message)
        player = data.get("pid")
        game.hit(player)

    def on_stand(self, message):
        game.advance()
    
    '''def on_game_event(self, message):
        data = dict(message)
        event = data.get("type")
        player = data.get("pid")
        match event:
            case "hit":
                game.hit(player)
            case "stand":
                game.advance()
            case _:
                pass
        print(f"{player} performed a {event}")'''
        


class Home(Namespace):
    def on_connect(self):
        print("test")
        
    

class Admin(Namespace):
    def on_connect(self):
        print("admin connected")
        return "connected"
    
    def on_start_game(self):
        global game
        print("starting game")
        game = Game(players, gameRoom)
        game.start()
        send("started", namespace="/admin")
        return "ok"
    