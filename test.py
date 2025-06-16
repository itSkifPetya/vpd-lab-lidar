from client.lidar import Lidar
import matplotlib.pyplot as plt
import time
uart_port = '/dev/ttyACM0'
uart_speed = 19200

LI = Lidar(uart_port, uart_speed, 1000)
while True:
    try:
        (x, y) = LI.get_single_scan_and_parse()
    finally:
        LI.close()
    plt.plot(x, y, '.')
    plt.show()
    time.sleep(0.5)