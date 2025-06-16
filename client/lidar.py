import serial
from numpy import array, cos, sin, pi
from hokuyo.driver import hokuyo
from hokuyo.tools import serial_port

class Lidar:
    def __init__(self, uart_port: str, uart_speed: int, timeout: int):
        self.__laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed, timeout=timeout)
        self.__port = serial_port.SerialPort(self.__laser_serial)
        self.__laser = hokuyo.Hokuyo(self.__port)
        self.__cloud = array()
        self.__xy = tuple()
        self.__data = []

    def __single_scan(self):
        self.__laser.laser_on()
        self.__cloud = self.__laser.get_single_scan()
        if self.__cloud == b'': return True
        return False
    
    def parse_single_scan(self):
        if self.__single_scan(): return True
        angle = array(list(self.__cloud.keys())) * pi/180
        dist = array(list(self.__cloud.values())) / 1000
        x = dist * cos(angle)
        y = dist * sin(angle)
        self.__xy = (x, y)
        self.__data.append(self.__xy)
        return False
    
    def get_xy(self):
        return self.__xy
    
    def close(self):
        self.__laser.reset()
        self.__laser.laser_off()
        self.__laser_serial.close()
    
