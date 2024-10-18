from flask_socketio import Namespace, emit, ConnectionRefusedError

class Playing(Namespace):

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        emit('my_response', data)


class Home(Namespace):
    def on_connect(self):
        print("test")
        raise ConnectionRefusedError('unauthorized!')
    

class Admin(Namespace):
    def on_connect(self):
        return "error"