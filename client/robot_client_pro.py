# Vpd Lab Lidar Client

import socket
import threading
import pickle
import time
from receiver import Receiver
from lidar import Lidar
# from hokuyo.driver import hokuyo
# from hokuyo.tools import serial_port

T = 0.02

UART_PORT = '/dev/ttyACM0'
UART_SPEED = 19200

HOST_ROBOT = "localhost"
PORT_ROBOT = 65432

stop_event = threading.Event()

def receiving_robot(RC: Receiver):
    while not stop_event.is_set():
        if RC.receive_pos(): continue
        
def receiving_cloud(LI: Lidar):
    while not stop_event.is_set():
        if LI.parse_single_scan(): continue

def concat_and_write_data(file, RC: Receiver, LI: Lidar): 
    while not stop_event.is_set():
        (x, y) = RC.get_xy()
        xy_cloud = LI.get_xy()
        # xy_cloud = []
        pickle.dump((x, y, xy_cloud), file)
        time.sleep(T)


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open("client/icp/data.csv", "wb") as f:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST_ROBOT, PORT_ROBOT))
        RC = Receiver(s, T)
        LI = Lidar(UART_PORT, UART_SPEED, 1000)
        robotThr = threading.Thread(target=receiving_robot, args=(RC, ), daemon=True)
        lidarThr = threading.Thread(target=receiving_cloud, args=(LI, ), daemon=True)
        writeThr = threading.Thread(target=concat_and_write_data, args=(f, RC, LI), daemon=True)

        robotThr.start()
        lidarThr.start()
        writeThr.start()
        
        input("Press Enter to stop...")
except Exception as e:
    print(f"Error {e}")
    # LI.close()
    # f.close()
    
finally:
    stop_event.set()
    lidarThr.join()
    robotThr.join()
    writeThr.join()
