import socket
import pickle
import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure(1)
ax = fig.add_subplot(111)

HOST = "localhost"
PORT = 65432

pos = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(4096)
        if data == b'': continue
        (x, y) = pickle.loads(data)
        # print(x, y)
        pos.append((x, y))
        ax.clear()
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.grid(True)
        xs, ys = zip(*pos)
        # print(xs, ys)
        ax.plot(xs, ys, marker='o')
        plt.draw()
        plt.pause(0.01)

plt.show()