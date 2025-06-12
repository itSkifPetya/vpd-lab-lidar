import pandas as pd
import matplotlib.pyplot as plt
from math import cos, sin
df = pd.read_json("data/single_scan_room.json")

angle = df[0]
dist = df[1]/1000

ndf = pd.DataFrame([d * cos(theta) for d in dist for theta in angle], [d * sin(theta) for d in dist for theta in angle])
# y = 

# print(ndf)

plt.figure()
plt.plot(ndf)
plt.show()