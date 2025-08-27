import numpy as np
import datetime

start = datetime.datetime.now()
# Parameters
rows, cols = 250, 250   # grid size
time_steps = 1000         # number of time steps

# Initialize the grid randomly (0=dead, 1=alive)
grid = np.random.randint(0, 2, size=(rows, cols))

# 3D array to store the states over time
history = np.zeros((time_steps, rows, cols), dtype=int)
history[0] = grid

# Function to count alive neighbors
def count_neighbors(grid, i, j):
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue  # skip the cell itself
            ni, nj = i + di, j + dj
            if 0 <= ni < grid.shape[0] and 0 <= nj < grid.shape[1]:
                count += grid[ni, nj]
    return count

# Simulation loop
for t in range(1, time_steps):
    new_grid = np.zeros_like(grid)
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(grid, i, j)
            if grid[i, j] == 1:  # alive
                if neighbors == 2 or neighbors == 3:
                    new_grid[i, j] = 1
            else:  # dead
                if neighbors == 3:
                    new_grid[i, j] = 1
    grid = new_grid
    history[t] = grid
end = datetime.datetime.now()
print(f"Time taken: {end - start}")
# Print the states
# for t in range(time_steps):
#     print(f"Step {t}:\n{history[t]}\n")
