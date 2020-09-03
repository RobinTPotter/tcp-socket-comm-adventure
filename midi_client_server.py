from threading import Thread
import pygame.midi as pm
import pickle
from client_server import client, server
from http.server import SimpleHTTPRequestHandler, HTTPServer




from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)


@socketio.on('hello')
def hello(data):
    print(data)


@socketio.on('noteon')
def noteon(data):
    print(data)


@socketio.on('noteoff')
def noteoff(data):
    print(data)


@app.route("/")
def index():
    keycodes = [65,66,67,68,69,70,71,72,73,74,75,76,77]
    keycolours = [0,1,0,1,0,0,1,0,1,0,1,0,0]
    keys = [a for a in zip(keycodes, keycolours, range(len(keycolours)))]
    keys = ''.join(["<div style=\"position:absolute; left:"+ str((k[2]*60)) +"\" class=\""+ ('w' if k[1]==0 else 'b') +"\" ontouchstart=\"down(event)\" ontouchend=\"up(event)\" onmousedown=\"down(event)\" onmouseup=\"up(event)\">"+ str(k[0]) +"</div>" for k in keys])
    return """<html onselectstart='return false;'>
<style>.w,.b {width:60px; height:60px; border: 1px solid black }
.w { background-color: white}
.b { background-color: black}
</style>
<body>
<script src=\"static/socketio.js\" crossorigin=\"anonymous\"></script>
<script type="text/javascript" charset="utf-8">
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('hello', {data: 'I\\'m connected!'});
    });
</script>
"""+keys+"""
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
</body></html>"""


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')



#server = HTTPServer(('', 12345), RubbishHandler)
#server.serve_forever()


'''
class KeyboardThread(Thread):
    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()
    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return
'''



class midigenclient(client):
    def __init__(self, ip, port):
        client.__init__(self, ip, port)

        #self.keymap = {
        #         pg.K_s: 1,  pg.K_s: 1,             pg.K_g: 6,  pg.K_h: 8,   pg.K_j: 10,
        #    pg.K_z: 0, pg.K_x: 2, pg.K_c: 4, pg.K_v: 5,  pg.K_b: 7,   pg.K_n: 9,   pg.K_m: 11, pg.K_COMMA: 12  
        #}
        self.kb = KeyboardThread(self.gomidi)
        self.transpose = 65
        self.octave = -1
        #self.mthread = Thread(None, self.gomidi)
        #self.mworking = True
        #self.mthread.start()

    def cleanup(self):
        self.working = False
        self.mthread.join()

    def gomidi(self, thing):
        print(thing)
        '''
        while self.mworking:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                    if event.type == pg.KEYDOWN:
                        if event.key in self.keymap:
                            self.sendall(pickle.dumps([0x90, self.keymap[event.key] + self.transpose + 12 * self.octave , 100]))
                    if event.type == pg.KEYUP:
                        if event.key in self.keymap:
                            self.sendall(pickle.dumps([0x80, self.keymap[event.key] + self.transpose + 12 * self.octave , 0]))
                            self.sendall(pickle.dumps([0x90, self.keymap[event.key] + self.transpose + 12 * self.octave , 0]))
        '''


# this is the thing that gets midi events and sends them to the other place in a pickle
class midiclient(client):
    def __init__(self, ip, port, desc='input'):
        client.__init__(self, ip, port)
        pm.init()
        try:
            self.device_num = [c for c in range(pm.get_count()) if desc in str(pm.get_device_info(c)[1]).lower()][0]
        except:
            raise Exception('no device named {} anywhere probably'.format(desc))
        self.device = Input(self.device_num)
        self.mthread = Thread(None, self.midi_me_up)
        self.mworking = True
        self.mthread.start()
    def midi_me_up(self):
        while self.mworking:
            if self.device.poll():
                data = self.device.read()
                self.sendall(pickle.dumps(data))
    def cleanup(self):
        client.cleanup(self)
        self.mworking = False
        self.mthread.join()
        self.device.close()

# this is the thing that expects midi events in a pickle and sends to fluidynth
class midiserver(server):
    def __init__(self, ip, port, desc='synth'):
        server.__init__(self, ip, port)
        pm.init()
        try:
            self.device_num = [c for c in range(pm.get_count()) if desc in str(pm.get_device_info(c)[1]).lower()][0]
        except:
            raise Exception('no device named {} anywhere probably'.format(desc))
        self.device = pm.Output(self.device_num)
    def msg_action(self, r):
        data = pickle.loads(r)
        self.device.write(data)
    def cleanup(self):
        server.cleanup(self)
        self.device.close()
