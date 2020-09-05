# TCP Socket Communication Adventure

learning about sockets in python

sending arbitrary bytes to another listening computer

no protocol, no police

![server example](./img/s.jpg)
![client example](./img/c.jpg)

# Midi Server

```
import midi_client_server
s=midi_client_server.midiserver('',12345,'u2midi')
s.stop()
```

# Midi Generating Client

Attaches to (already running server)

```
import midi_client_server
c=midi_client_server.midigenclient('192.168.1.76',12345)
c.noteon(65,50)
c.noteoff(65)
```

These two seem to be OK together


# Flask Piano

Web page keyboard at port 5000, use callback functions to attach to midigenclient:

```
import flask_piano
f=flask_piano.flask_piano()

def on(data):
 c.noteon(int(data['data']),50)
def off(data):
 c.noteoff(int(data['data']))

f.noteon_callback=on
f.noteoff_callback=off
f.run()
```

Results are very underwhelming at the moment, probably socket comms too slow for socketio

