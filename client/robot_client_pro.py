# Vpd Lab Lidar Client

import socket
import threading
import pickle
import matplotlib.pyplot as plt
from receiver import Receiver
from lidar import Lidar
from hokuyo.driver import hokuyo
from hokuyo.tools import serial_port

T = 0.02

UART_PORT = 'COM4'
UART_SPEED = 19200

HOST_ROBOT = "localhost"
PORT_ROBOT = 65432

def receiving_robot(RC: Receiver):
    while True:
        if RC.receive_pos(): continue
        
def receiving_cloud(LI: Lidar):
    while True:
        if LI.parse_single_scan(): continue

def concat_and_write_data(file):
    while True:
        (x, y) = RC.get_xy()
        xy_cloud = LI.get_xy()
        pickle.dump((x, y, xy_cloud), file)
stop_event = threading.Event()


try:
    with socket(socket.AF_INET, socket.SOCK_STREAM) as s, open("data.csv", "w+") as f:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST_ROBOT, PORT_ROBOT))
        RC = Receiver(s, T)
        LI = Lidar(UART_PORT, UART_SPEED, T*1000)
        robotThr = threading.Thread(target=receiving_robot, args=(RC, ), daemon=True)
        lidarThr = threading.Thread(target=receiving_cloud, args=(LI, ), daemon=True)
        writeThr = threading.Thread(target=concat_and_write_data, args=(f, ), daemon=True)

        robotThr.start()
        lidarThr.start()
        writeThr.start()
        
except Exception as e:
    LI.close()
    
try: 
    input("Press Enter to stop...")
finally:
    stop_event.set()
    lidarThr.join()
    robotThr.join()
    writeThr.join()
