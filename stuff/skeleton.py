#### "client"

import socket
import threading

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.80',12345)) # where they are waiting for you

def msg_recieved(client):
 while True: print(client.recv(100))

# start thread to print out messages from the socket, these messages are from "server"
rthread = threading.Thread(None, msg_recieved, args = (s,))
rthread.start()

s.sendall(b'bollocks!')

#### "server"

import threading
import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('',12345))
s.listen()
client, address = s.accept()

def msg_recieved(client):
 while True: print(client.recv(100))

# start thread to print out messages from the "client" (they that we accepted when they connected)
rthread = threading.Thread(None, msg_recieved, args = (client, ))
rthread.start()

client.sendall(b'oi bollocks')
