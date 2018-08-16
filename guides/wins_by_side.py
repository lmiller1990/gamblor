import pandas as pd

df = pd.read_csv("data.csv")

victories = df[df['result'] == 1]
total_wins = df.shape[0]/2
red = victories[victories['side'] == 'Red'].shape[0]
blue = victories[victories['side'] == 'Blue'].shape[0]

print('Red victories', blue, (blue / total_wins) * 100)
print('Red victories', red, (red / total_wins) * 100)
