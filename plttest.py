import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure(1)
ax = fig.add_subplot(111)

pos = []
# x = []
# y = []
l = list(range(-3, 3))
for i in range(len(l)):
    pos.append((l[i], l[i]))
    print(pos)
    # x.append(l[i])
    # y.append(l[i])
    ax.clear()
    ax.set_xlim([-4, 4])   # задаём масштаб после clear
    ax.set_ylim([-4, 4])
    ax.grid(True)
    ax.plot(pos, marker='o')
    plt.draw()
    plt.pause(0.5)
plt.show(block=True)