import serial

from hokuyo.driver import hokuyo
from hokuyo.tools import serial_port

import time
import matplotlib.pyplot as plt
import math

uart_port = '/dev/ttyACM0'
uart_speed = 19200

if __name__ == '__main__':
    laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed, timeout=0.5)
    port = serial_port.SerialPort(laser_serial)

    laser = hokuyo.Hokuyo(port)

    laser.reset()
    laser.laser_off()

    laser.laser_on()

    
    # data = laser.get_single_scan()
    # x = []
    # y = []
    # f = open("scan.csv", "w+")
    # # print(data.items())
    # for key, value in data.items():
    #     # f.write(f"{key},{value}\n")
    #     ang = key * math.pi/180
    #     val = value / 1000
    #     f.write(f"{ang},{val}\n")
    #     x.append(val*math.cos(ang))
    #     y.append(val*math.sin(ang))

    # ax.scatter(x, y, s=2)
    # plt.xlim([-1, 1])
    # plt.ylim([-1, 1])
    
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    # for i in range(100):
    while True:
        data = laser.get_single_scan()
        x = []
        y = []
        for key, value in data.items():
            ang = key * math.pi/180
            val = value / 1000
            x.append(val*math.cos(ang))
            y.append(val*math.sin(ang))

        ax.clear()
        # ax.scatter(x, y, s=2)
        # ax.scatter(x, y, s=2)
        ax.plot(x, y, marker='.', linestyle='', markersize=2)
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        # data = laser.get_single_scan()
        # x = []
        # y = []
        # for key, value in data.items():
        #     ang = key * math.pi/180
        #     x.append(value*math.cos(ang))
        #     y.append(value*math.sin(ang))

        # ax.clear()
        # ax.scatter(x, y, s=2)

        # time.sleep(0.01)
        plt.grid(True)
        plt.draw()
        plt.pause(0.01)
    
    #     time.sleep(0.01)
    
    print(laser.reset())
    print(laser.laser_off())

    # print(laser.laser_on())
    # print('---')
    # print(laser.get_single_scan())
    # print('---')
    # print(laser.get_version_info())
    # print('---')
    # print(laser.get_sensor_specs())
    # print('---')
    # print(laser.get_sensor_state())
    # print('---')
    # print(laser.set_high_sensitive())
    # print('---')
    # print(laser.set_high_sensitive(False))
    # print('---')
    # print(laser.set_motor_speed(10))
    # print('---')
    # print(laser.set_motor_speed())
    # print('---')
    # print(laser.reset())
    # print('---')
    # print(laser.laser_off())