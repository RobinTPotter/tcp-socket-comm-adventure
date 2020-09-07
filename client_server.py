import socket
import threading
import abc

class Common(abc.ABC):    
    def __init__(self, ip, port=12345):            
        self.working = True
        self.init(ip, port)
        self.start()
    @abc.abstractmethod
    def init(self, ip, port):
        pass
    @abc.abstractmethod
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
            if len(r)>0: self.msg_action(r)
    def msg_action(self,r):
        print(r)
    def stop(self):
        self.working = False
        self.s.close()
        self.cleanup()
        self.rthread.join()
        print('closed, joined, stopped')
    def sendall(self, msg):
        self.s.sendall(msg)
    
class Client(Common):    
    def init(self, ip, port):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip,port))
        self.s.setblocking(0)
    def cleanup(self):
        pass

class Server(Common):    
    def init(self, ip, port):
        if ip==None: ip=''
        self.srv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.bind((ip,port))
        self.srv.listen()
        self.s, self.address = self.srv.accept()
        self.s.setblocking(0)
    def cleanup(self):
        self.srv.close()


