from flask import Flask, render_template, request
from flask_socketio import SocketIO

class FlaskPiano():
    """run a flask webserver on a device and access a piano page notes 65-77
    """
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.app.add_url_rule('/', 'index', self.index)
        self.socketio = SocketIO(self.app)
        self.socketio.on_event('hello', self.hello)
        self.socketio.on_event('noteon', self.noteon)
        self.socketio.on_event('noteoff', self.noteoff)
        self.socketio.on_event('oct_up', self.oct_up)
        self.socketio.on_event('oct_down', self.oct_down)        
        self.noteon_callback = None
        self.noteoff_callback = None
        self.transpose = 0

    def run(self, host='0.0.0.0'):
        """run the webserver

        Args:
            host (str, optional): listening host. Defaults to '0.0.0.0'.
        """
        self.socketio.run(self.app, host=host)

    def hello(self, data):
        """used when page is loaded (ie client connects)

        Args:
            data (str): message from page (see page body below)
        """
        print('hello {}'.format(request.remote_addr))

    def noteon(self, data):
        """send note on, prints if noteon_callback is none.

        Args:
            data ([json]): a json object with note data
        """
        if self.noteon_callback==None: print(data)
        else: self.noteon_callback(data)

    def noteoff(self, data):
        """send note off, prints if noteoff_callback is none.

        Args:
            data ([json]): a json object with note data
        """
        if self.noteoff_callback==None: print(data)
        else: self.noteoff_callback(data)

    def oct_up(self, data):
        """Set the transpose value + 12."""
        self.transpose += 12

    def oct_down(self, data):
        """Set the transpose value - 12."""
        self.transpose -= 12

    def index(self):
        """the page revealing piano notes, also some buttons, buttons are
        drawn with their current values, taking into account the transpose
        value
        """

        keycodes = [65,66,67,68,69,70,71,72,73,74,75,76,77]
        keycolours = [0,1,0,1,0,0,1,0,1,0,1,0,0]
        keys = [a for a in zip(keycodes, keycolours, range(len(keycolours)))]
        keys = ''.join(["<div style=\"position:absolute; left:" + \
            str((k[2]*60)) + "\" class=\""+ ('w' if k[1]==0 else 'b') + \
            "\" ontouchstart=\"down(event)\" ontouchend=\"up(event)\" onmousedown=\"down(event)\" onmouseup=\"up(event)\">"+ str(k[0] + self.transpose) +"</div>" for k in keys])
        return """<html onselectstart='return false;'>
            <style>.w,.b,.btn {width:60px; height:60px; border: 1px solid black }
            .w { background-color: white}
            .b { background-color: black}
            </style>
            <meta content='width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=no;' name='viewport' />
            <body>
            <script src=\"static/socketio.js\" crossorigin=\"anonymous\"></script>
            <script type="text/javascript" charset="utf-8">
            var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
                socket.on('connect', function() {
                    socket.emit('hello', {data: 'I\\'m connected!'});
                });
            </script>
            """ + keys + """
            <div style="position:absolute; top:80px; left:10px" class="btn" ontouchstart="oct_up_down(event)" ontouchend="oct_up_up(event)" onmousedown="oct_up_down(event)" onmouseup="oct_up_up(event)">O+</div>
            <div style="position:absolute; top:80px; left:70px" class="btn" ontouchstart="oct_down_down(event)" ontouchend="oct_down_up(event)" onmousedown="oct_down_down(event)" onmouseup="oct_down_up(event)">O-</div>
            <script>
            function down(e) {
            e.srcElement.style.backgroundColor = "red" 
            socket.emit('noteon', {data: e.srcElement.innerText })
            }
            function up(e) {
            col = "black"
            if (e.srcElement.classList.contains('w')) col = "white"
            e.srcElement.style.backgroundColor = col
            socket.emit('noteoff', {data: e.srcElement.innerText })
            }
            function oct_up_down(e) {
            e.srcElement.style.backgroundColor = "red" 
            socket.emit('oct_up', {data: e.srcElement.innerText })
            }
            function oct_up_up(e) {
            e.srcElement.style.backgroundColor = "white"
            setTimeout(function() {
              location.reload()
            }, 200)
            }
            function oct_down_down(e) {
            e.srcElement.style.backgroundColor = "red" 
            socket.emit('oct_down', {data: e.srcElement.innerText })
            }
            function oct_down_up(e) {
            e.srcElement.style.backgroundColor = "white"
            setTimeout(function() {
              location.reload()
            }, 200)
            }
            </script>
            </body></html>
        """


