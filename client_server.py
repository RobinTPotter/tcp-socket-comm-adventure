# # classy
# just been learing about abc, clever if you like that sort of thing
# common class creates the thread for the receipt of messages to print
# client overrides the init function to connect the socket s to to a listening "server"
# server overrides init to create a srv socket (the server),
# while s represeents the attached client
# the cleanup function is overridden to allow the srv socket to be closed.
# 
# usage:
# 
# import client_server
# s = client_server.server('',12345)
# # blocks until client attaches
# s.sendall(b'bollocks')
# 
# or:
# 
# import client_server
# c = client_server.client('localhost',12345)
# c.sendall(b'bollocks')




import socket
import threading
import abc

class common(abc.ABC):    
    def __init__(self, ip, port=12345):            
        self.working = True
        self.init(ip, port)
        self.start()
    @abc.abstractmethod
    def init(self, ip, port):
        pass
    def cleanup(self):
        pass
    def start(self):
        # start thread to print out messages from the socket, these messages are from "server"
        self.rthread = threading.Thread(None, self.msg_recieved)
        self.rthread.start()
    def msg_recieved(self):
        while self.working:
            r = b''
            #print('waitn')
            try:
                r = self.s.recv(1024)
            except:
                pass
            # print('recvd')
            if len(r): print(r)
        print("end")
    def stop(self):
        self.working = False
        self.s.close()
        self.cleanup()
        self.rthread.join()
        print('closed, joined, stopped')
    def sendall(self, msg):
        self.s.sendall(msg)
    
class client(common):    
    def init(self, ip, port):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip,port))
        self.s.setblocking(0)

class server(common):    
    def init(self, ip, port):
        if ip==None: ip=''
        self.srv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.bind((ip,port))
        self.srv.listen()
        self.s, self.address = self.srv.accept()
        self.s.setblocking(0)
    def cleanup(self):
        self.srv.close()


