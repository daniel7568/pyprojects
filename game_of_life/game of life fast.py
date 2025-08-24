import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import datetime
import numba as nb


start = datetime.datetime.now()
N = 100
T = 6000
grid = np.random.randint(0,2,(N+1,N+1))
grid[0,:] = 0
grid[-1,:] = 0
grid[:,0] = 0
grid[:,-1] = 0


def new_frame(frame):
    return plt.imshow(states[frame,:,:])

@nb.njit
def update(grid, T):
    N = grid.shape[0]
    states = np.empty((T, N, N), dtype=np.uint8)
    states[0] = grid
    for t in range(1, T):
        new_grid = np.zeros_like(grid)
        for i in range(1, N-1):
            for j in range(1, N-1):
                total = np.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
                if total == 3 or (grid[i, j] == 1 and total == 2):
                    new_grid[i, j] = 1
        grid = new_grid
        states[t] = grid
    return states

states = update(grid, T)

end = datetime.datetime.now()

print(f"Time taken: {end - start}")
fig = plt.figure()
anim = animation.FuncAnimation(fig, new_frame,frames=range(T))
anim.save("life_game_animation.mp4","ffmpeg")
