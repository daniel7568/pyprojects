import numpy as np
from itertools import product
import pickle
array = np.empty((3,3))

def f(mtx):
    s = np.sum(mtx)
    if mtx[1,1] == 0:
        if s==3:
            return 1
        else:
            return 0
    elif s>2 and s<5:
        return 1
    return 0

memo = {}

for combo in product([0, 1], repeat=9):
    array[:] = np.array(combo,dtype=int).reshape(3,3)
    print(array)
    memo[tuple(array.ravel())] = f(array)


test = np.array([[0,0,1],[1,0,1],[0,0,0]])
print(test)
print(memo[tuple(test.ravel())])

with open("memo.pkl", 'wb') as f:
    pickle.dump(memo,f)
