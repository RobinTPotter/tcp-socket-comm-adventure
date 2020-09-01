import pygame.midi as pm
import pickle
from client_server import client, server

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
                self.sendall(pickle.dumps(data)))
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
