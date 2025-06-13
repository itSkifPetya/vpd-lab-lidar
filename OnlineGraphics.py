import serial
from hokuyo.driver import hokuyo
from hokuyo.tools import serial_port
import time
import matplotlib.pyplot as plt
import math
import numpy as np

uart_port = 'COM4'
uart_speed = 19200
# 

T = 0.5
try:

    laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed, timeout= 1000)
    port = serial_port.SerialPort(laser_serial)
    laser = hokuyo.Hokuyo(port)
    filename = 'data_laser.csv'

    laser.laser_on()
    startTime = time.time()
    N = 0

    plt.ion()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    data = laser.get_single_scan()
    print(data)

    if data == b'':
        raise RuntimeError("socket connection broken")
    
    ang = np.array(list(data.keys())) * np.pi/180
    dist = np.array(list(data.values())) / 1000
    x = dist * np.cos(ang)
    y = dist * np.sin(ang)
    print(x)

    sc = ax.scatter(x, y, s=2)
    plt.xlim([-4, 4])
    plt.ylim([-4, 4])
    plt.grid(True)
    # plt.show(block=True)
    plt.pause(1)
    
    while time.time() - startTime < 30:
        data = laser.get_single_scan()

        if data == b'':
            raise RuntimeError("socket connection broken")
        
        ang = np.array(list(data.keys())) * np.pi/180
        dist = np.array(list(data.values())) / 1000
        print(dist.shape)
        x = dist * np.cos(ang)
        y = dist * np.sin(ang)

        ax.clear()
        ax.scatter(x, y, s=2)
        plt.xlim([-4, 4])
        plt.ylim([-4, 4])
        plt.grid(True)
        plt.pause(0.1)
        print("update",time.time())

        N += 1

except Exception as e:
    raise e
finally:
    laser.reset()
    laser.laser_off()
    laser_serial.close()
