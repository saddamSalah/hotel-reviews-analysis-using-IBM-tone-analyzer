import pandas as pd

df = pd.read_csv('../Data/7282_1.csv')
print(df.head())
print(df.shape)
df = df.loc[df['categories'] == 'Hotels']
print(df.shape)
df.to_csv('../Data/hotels.csv')