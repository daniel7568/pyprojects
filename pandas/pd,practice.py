import pandas as pd
import numpy as np
coffee = pd.read_csv("https://raw.githubusercontent.com/KeithGalli/complete-pandas-tutorial/refs/heads/master/warmup-data/coffee.csv")
result = pd.read_parquet('./data/results.parquet')
bios = pd.read_csv("./data/bios.csv")

#print(bios.query('name=="Daniel"'))
#print(bios.query('name.str.startswith("Daniel")'))
coffee["price"] = np.where(coffee['Coffee Type'] == 'Espresso',3.99,5.99)
print(coffee.head())
print(coffee["price"].sum())