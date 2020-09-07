import eventlet
import socketio

class socket_server:
    def __init__(self):
        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(self.sio, static_files={
            '/': {'content_type': 'text/html', 'filename': 'index.html'}
        })
    @sio.event
    def connect(sid, environ):
        print('connect ', sid)
    @sio.event
    def my_message(sid, data):
        print('message ', data)
    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)

