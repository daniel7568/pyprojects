import numpy as np
import matplotlib.pyplot as plt
import pickle as pl
from matplotlib import animation
import datetime



start = datetime.datetime.now()
N = 100
T = 120
states = np.empty((T,N+1,N+1))
grid = np.random.randint(0,2,(N+1,N+1))
grid[0,:] = 0
grid[-1,:] = 0
grid[:,0] = 0
grid[:,-1] = 0
states[0] = grid

def new_frame(frame):
    return plt.imshow(states[frame,:,:])

def check(mtx):
    return memo[tuple(mtx.ravel())]

with open("memo.pkl", "rb") as f:
    memo = pl.load(f)

for t in range(1,T):
    for i in range(1,N-1):
        for j in range(1,N-1):
            grid[i,j] = check(grid[i-1:i+2,j-1:j+2])
    states[t,:,:] = grid
end = datetime.datetime.now()

print(f"Time taken: {end - start}")
fig = plt.figure()
anim = animation.FuncAnimation(fig, new_frame,frames=range(T))
#anim.save("life_game_animation.mp4","ffmpeg")
plt.show()