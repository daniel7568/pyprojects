import math
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from numba import jit

@jit(nopython=True)
def compute_trajectory(ship_speed, torpedo_speed, ax, ay, az):
    dt = 0.000001  # Time step
    max_time = 300  # Maximum simulation time
    max_steps = int(max_time / dt)  # Maximum possible steps based on time and dt
    ship_trajectory = np.zeros((max_steps, 3), dtype=np.float64)
    torpedo_trajectory = np.zeros((max_steps, 3), dtype=np.float64)

    # Initialize positions and velocities
    ship_pos = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    ship_direction = np.array([random.uniform(-1, 1), random.uniform(-1, 1), 0.0], dtype=np.float64)
    ship_direction /= np.linalg.norm(ship_direction)
    ship_vel = ship_direction * ship_speed
    torpedo_pos = np.array([ax, ay, az], dtype=np.float64)

    # Start recording trajectories
    ship_trajectory[0] = ship_pos
    torpedo_trajectory[0] = torpedo_pos
    time = 0
    intersection_point = None
    step = 1

    while step < max_steps:
        time += dt
        # Update ship position
        new_ship_pos = ship_pos + ship_vel * dt
        new_ship_pos[2] = 0  # Ensure ship stays on the surface
        ship_pos = new_ship_pos
        ship_trajectory[step] = ship_pos

        # Occasionally randomize ship direction
        if random.random() < 0.000002:
            new_direction = np.array([random.uniform(-1, 1), random.uniform(-1, 1), 0.0], dtype=np.float64)
            new_direction /= np.linalg.norm(new_direction)
            ship_vel = new_direction * ship_speed

        # Update torpedo position
        torpedo_direction = (ship_pos - torpedo_pos) / np.linalg.norm(ship_pos - torpedo_pos)
        torpedo_vel = torpedo_direction * torpedo_speed
        torpedo_pos = torpedo_pos + torpedo_vel * dt
        torpedo_trajectory[step] = torpedo_pos

        # Check for collision
        distance = np.linalg.norm(ship_pos - torpedo_pos)
        if distance < 10:
            intersection_point = torpedo_pos
            break

        step += 1

    # Return only the filled portion of the arrays
    return ship_trajectory[:step], torpedo_trajectory[:step], intersection_point

def plot_trajectory(ship_trajectory, torpedo_trajectory, intersection_point, az):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ship_x, ship_y, ship_z = ship_trajectory.T
    torpedo_x, torpedo_y, torpedo_z = torpedo_trajectory.T

    ax.plot(ship_x, ship_y, ship_z, label='Ship', color='blue')
    ax.plot(torpedo_x, torpedo_y, torpedo_z, label='Torpedo', color='green')

    if intersection_point is not None:
        ax.scatter([intersection_point[0]], [intersection_point[1]], [intersection_point[2]],
                   color='red', s=100, label='Intersection')

    x = np.linspace(min(ship_x + torpedo_x), max(ship_x + torpedo_x), 50)
    y = np.linspace(min(ship_y + torpedo_y), max(ship_y + torpedo_y), 50)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    ax.plot_surface(X, Y, Z, color='c', alpha=0.5, rstride=100, cstride=100, label='Surface')

    ax.set_xlabel('X position (m)')
    ax.set_ylabel('Y position (m)')
    ax.set_zlabel('Z position (m)')
    ax.legend()
    ax.set_title('3D Torpedo Hit Simulation (Ship on Surface)')

    max_range = np.array([max(ship_x+torpedo_x)-min(ship_x+torpedo_x),
                          max(ship_y+torpedo_y)-min(ship_y+torpedo_y),
                          max(torpedo_z)-min(torpedo_z)]).max() / 2.0
    mid_x = (max(ship_x+torpedo_x)+min(ship_x+torpedo_x)) * 0.5
    mid_y = (max(ship_y+torpedo_y)+min(ship_y+torpedo_y)) * 0.5
    mid_z = (max(torpedo_z)+min(torpedo_z)) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(az, mid_z + max_range)
    plt.show()

start1 = time.time()
ship_trajectory, torpedo_trajectory, intersection_point = compute_trajectory(60, 70, 250, 500, -500)
end = time.time()
print(end - start1)

# Plotting the results
plot_trajectory(ship_trajectory, torpedo_trajectory, intersection_point, -500)