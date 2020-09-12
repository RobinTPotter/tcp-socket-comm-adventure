from threading import Thread
import time
import pygame.midi as pm
import pickle
from client_server import Client, Server
from http.server import SimpleHTTPRequestHandler, HTTPServer

# this then generates (pygame) midi events, can be used as a callback for the flask_piano
class MidiGenClient(Client):
    def __init__(self, ip, port):
        Client.__init__(self, ip, port)
        self.transpose = 0
        self.octave = 0
    def cleanup(self):
        self.working = False
        self.mthread.join()
    def noteon(self, note, vel=100):
        #p=pickle.dumps([[[0x90, note + self.transpose + 12 * self.octave, vel],time.time()]])
        #self.sendall(p)
        self.sendall(bytes([0x90, note + self.transpose + 12 * self.octave, vel]))
        #print(p)
    def noteoff(self, note):
        #self.sendall(pickle.dumps([[[0x80, note + self.transpose + 12 * self.octave, 0], time.time()]]))
        #self.sendall(pickle.dumps([[[0x90, note + self.transpose + 12 * self.octave, 0], time.time()]]))
        self.sendall(bytes([0x80, note + self.transpose + 12 * self.octave]))
        self.sendall(bytes([0x90, note + self.transpose + 12 * self.octave, 0]))

# this is the thing that gets midi events and sends them to the other place in a pickle
class MidiDevClient(Client):
    def __init__(self, ip, port, desc='input'):
        Client.__init__(self, ip, port)
        pm.init()
        try:
            self.device_num = [c for c in range(pm.get_count()) if desc.lower() in str(pm.get_device_info(c)[1]).lower() and pm.get_device_info(c)[2]==1][0]
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
                print('disabled sendall {}'.format(data))
                #self.sendall(pickle.dumps(data))
    def cleanup(self):
        Client.cleanup(self)
        self.mworking = False
        self.mthread.join()
        self.device.close()

# this is the thing that expects midi events in a pickle and sends to fluidynth
class MidiServer(Server):
    def __init__(self, ip, port, desc='synth'):
        Server.__init__(self, ip, port)
        pm.init()
        try:
            self.device_num = [c for c in range(pm.get_count()) if desc.lower() in str(pm.get_device_info(c)[1]).lower() and pm.get_device_info(c)[3]==1][0]
        except:
            raise Exception('no device named {} anywhere probably'.format(desc))
        self.device = pm.Output(self.device_num)
    def msg_action(self, r):
        print(r)
        #data = pickle.loads(r)
        #self.device.write(data)
        datas = [d for d in r]
        if len(datas) == 1: self.device.write_short(datas[0])
        elif len(datas) == 2: self.device.write_short(datas[0],datas[1])
        elif len(datas) == 3: self.device.write_short(datas[0],datas[1],datas[2])
        elif len(datas) == 4: self.device.write_short(datas[0],datas[1],datas[2],datas[3])
    def cleanup(self):
        Server.cleanup(self)
        self.device.close()
