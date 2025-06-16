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


    laser.laser_on()

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    data = laser.get_single_scan()
    x = []
    y = []
    for key, value in data.items():
        ang = key * math.pi/180
        val = value / 1000
        x.append(val*math.cos(ang))
        y.append(val*math.sin(ang))

    ax.scatter(x, y, s=2)
    plt.xlim([-4, 4])
    plt.ylim([-4, 4])
    plt.grid(True)
    # plt.show()

    for i in range(100):
        data = laser.get_single_scan()
        x = []
        y = []
        for key, value in data.items():
            ang = key * math.pi/180
            x.append(value*math.cos(ang))
            y.append(value*math.sin(ang))

        ax.clear()
        ax.scatter(x, y, s=2)

        time.sleep(0.01)
    
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