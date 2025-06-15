import pandas as pd
import matplotlib.pyplot as plt
from math import cos, sin

def data_convert(df: pd.DataFrame) -> pd.DataFrame:
    angle = round(df[0], 4)
    dist = df[1]/1000
    ndf = pd.DataFrame({'x':[d * cos(theta) for d, theta in zip(dist, angle)], 'y':[d * sin(theta) for d, theta in zip(dist, angle)]})
    return ndf.round(4)
# print(data_convert(pd.read_json("data/single_scan_room.json")))
pd1 = pd.read_json("data/single_scan_room.json")
print(data_convert(pd1))

data_convert(pd.read_json("data/single_scan_room.json")).to_csv("data.csv", index=False)
data_convert(pd.read_json("data/single_scan_moved.json")).to_csv("data2.csv", index=False)