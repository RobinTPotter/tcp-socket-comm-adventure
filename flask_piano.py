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
        self.noteon_callback = None
        self.noteoff_callback = None

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

    def index(self):
        """the page revealing piano notes
        """

        keycodes = [65,66,67,68,69,70,71,72,73,74,75,76,77]
        keycolours = [0,1,0,1,0,0,1,0,1,0,1,0,0]
        keys = [a for a in zip(keycodes, keycolours, range(len(keycolours)))]
        keys = ''.join(["<div style=\"position:absolute; left:"+ str((k[2]*60)) +"\" class=\""+ ('w' if k[1]==0 else 'b') +"\" ontouchstart=\"down(event)\" ontouchend=\"up(event)\" onmousedown=\"down(event)\" onmouseup=\"up(event)\">"+ str(k[0]) +"</div>" for k in keys])
        return """<html onselectstart='return false;'>
            <style>.w,.b {width:60px; height:60px; border: 1px solid black }
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
            </script>
            </body></html>
        """


