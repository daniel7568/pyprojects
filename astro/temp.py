import csv
from mpmath import *

mp.dps = 10_000

with open("results.csv",'r') as f:
    reader = csv.reader(f)
    data = list(reader)

data.pop(0)
print(data[0][0])
b1 = mpmathify(data[0][0])
a1 = mpmathify(data[0][1])
b2 = mpmathify(data[1][0])
a2 = mpmathify(data[1][1])

print(fsub(b1,b2))