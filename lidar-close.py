from hokuyo.driver import hokuyo
from hokuyo.tools import serial_port
import serial

uart_port = '/dev/ttyACM0'
uart_speed = 19200
laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed, timeout=0.5)
port = serial_port.SerialPort(laser_serial)
laser = hokuyo.Hokuyo(port)
laser.reset()
laser.laser_off()