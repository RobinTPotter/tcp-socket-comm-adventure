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
