import pickle
import socket
import time

class Receiver:
    def __init__(self, s: socket.socket, T: int):
        self.x = 0
        self.y = 0
        self.pos = []
        self.socket = s
        self.isEmpty = True
        self.T = T
    
    def receive_pos(self):
        data = self.socket.recv(4096)
        if data == b'': return True
        (self.x, self.y) = pickle.loads(data)
        self.pos.append((self.x, self.y))
        # time.sleep(self.T)
        return False
    
    def get_xy(self):
        return (self.x, self.y)
    
    def get_pos(self):
        return self.pos