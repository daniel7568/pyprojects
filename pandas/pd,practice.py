import pandas as pd

coffee = pd.read_csv("https://raw.githubusercontent.com/KeithGalli/complete-pandas-tutorial/refs/heads/master/warmup-data/coffee.csv")
result = pd.read_parquet('./data/results.parquet')
bios = pd.read_csv("./data/bios.csv")

print(coffee)
#print(coffee.sum([]))
