import pandas as pd
import numpy as np

size = 20


# print(np.linspace(0, 20))
df1 = pd.DataFrame({'x': np.full(60, 0), 'y': np.linspace(0, 20, 60)})
df2 = pd.DataFrame({'x': np.linspace(0, 20, 60), 'y': np.full(60, 20)})
df3 = pd.DataFrame({'x': np.full(60, 20), 'y': np.linspace(20, 0, 60)})
df = pd.concat([df1, df2, df3])

df.to_csv("square.csv", index=False)
print(df)