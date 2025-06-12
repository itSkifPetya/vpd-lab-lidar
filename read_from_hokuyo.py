import serial

ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=5000)
print("connected to: " + ser.portstr)

while True:
    print('data')
    data = ser.read()
    print(data)
    print('test')