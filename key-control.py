# import time  
# import termios  
# import tty  
import time
import threading
import socket
# import struct
import pickle
from math import pi
import ev3dev2.motor as motor
# import sys
from keycontrol import KeyController
from odometry import Odometry

HOST = "localhost"
PORT = 65432

L_MOTOR = motor.LargeMotor(motor.OUTPUT_C)
R_MOTOR = motor.LargeMotor(motor.OUTPUT_B)

WHEEL_RADIUS = 5.6/2 / 100
BASE = 11.2 / 100
T = 0.02

OD = Odometry(WHEEL_RADIUS, BASE, T)

KC = KeyController(L_MOTOR, R_MOTOR, forward_cycle=60, turn_cycle=40)

def send_pos(x, y, client_sock: socket.socket):
    pos = pickle.dumps((x, y))
    sent = client_sock.send(pos)
    if sent == 0: raise RuntimeError("socket connection broken")

def odometry_sender(conn):
    while True:
        st = time.time()
        (x, y, _) = OD.update(L_MOTOR.speed * pi/180, R_MOTOR.speed * pi/180)
        try:
            send_pos(x, y, conn)
        except RuntimeError as e:
            print(e)
            L_MOTOR.stop()
            R_MOTOR.stop()
            break
        dt = T - (time.time() - st)
        if dt < 0: print("warning")
        else: time.sleep(dt)

def controller(controller: KeyController):
    while True:
        st = time.time()
        if controller.control(): break
        dt = T - (time.time() - st)
        if dt < 0: print("warning", end='\r', flush=True)
        else: time.sleep(dt)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for connection")
        conn, addr = s.accept()
        with conn:
            print("Connected by {}".format(addr))
            print("Ready to go!")

            sender_thr = threading.Thread(target=odometry_sender, args=(conn,), daemon=True)
            controller_thr = threading.Thread(target=controller, args=(KC,), daemon=True)
            try:
                sender_thr.start()
                controller_thr.start()
                controller_thr.join()
            except Exception as e:
                print(e)
                L_MOTOR.stop()
                R_MOTOR.stop()
            # while True:
                # if KC.control(): break
                # (x, y) = odometry()
                # try:
                #     send_pos(x, y, conn)
                # except RuntimeError as e:
                #     print(e)
                #     L_MOTOR.stop()
                #     R_MOTOR.stop()
                #     break
except Exception as e:
    L_MOTOR.stop()
    R_MOTOR.stop()