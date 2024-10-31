import math
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x/mag, self.y/mag, self.z/mag)

def calculate_direction(p1, p2):
    return Vector3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z).normalize()

def torpedo_hit_3d(ship_speed, torpedo_speed, ax, ay, az):
    dt = 0.1  # Time step
    max_time = 300  # Maximum simulation time
    ship_pos = Vector3D(0, 0, 0)
    ship_direction = Vector3D(random.uniform(-1, 1), random.uniform(-1, 1), 0).normalize()
    ship_vel = ship_direction * ship_speed
    torpedo_pos = Vector3D(ax, ay, az)
    ship_trajectory = [ship_pos]
    torpedo_trajectory = [torpedo_pos]
    time = 0
    intersection_point = None

    while True:
        time += dt
        # Move ship on the x-y plane (z = 0)
        new_ship_pos = ship_pos + ship_vel * dt
        new_ship_pos.z = 0  # Ensure ship stays on the surface
        ship_pos = new_ship_pos
        ship_trajectory.append(ship_pos)

        # Randomly change ship direction occasionally
        if random.random() < 0.02:  # 2% chance each step
            new_direction = Vector3D(random.uniform(-1, 1), random.uniform(-1, 1), 0).normalize()
            ship_vel = new_direction * ship_speed

        # Calculate torpedo direction and move
        torpedo_direction = calculate_direction(torpedo_pos, ship_pos)
        torpedo_vel = torpedo_direction * torpedo_speed
        torpedo_pos = torpedo_pos + torpedo_vel * dt
        torpedo_trajectory.append(torpedo_pos)

        # Check for collision
        distance = (ship_pos + torpedo_pos * -1).magnitude()
        if distance < 10:  # Assume hit within 10 meters
            print(f"Hit at time: {time:.2f} seconds")
            intersection_point = torpedo_pos
            break

        if time >= max_time:
            print("Maximum simulation time reached without a hit")
            break

    # Plotting
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ship_x = [p.x for p in ship_trajectory]
    ship_y = [p.y for p in ship_trajectory]
    ship_z = [p.z for p in ship_trajectory]
    torpedo_x = [p.x for p in torpedo_trajectory]
    torpedo_y = [p.y for p in torpedo_trajectory]
    torpedo_z = [p.z for p in torpedo_trajectory]

    ax.plot(ship_x, ship_y, ship_z, label='Ship', color='blue')
    ax.plot(torpedo_x, torpedo_y, torpedo_z, label='Torpedo', color='green')

    if intersection_point:
        ax.scatter(0,0,0,c="b",s=100)
        ax.scatter([intersection_point.x], [intersection_point.y], [intersection_point.z],
                   color='red', s=100, label='Intersection')

    # Create a semi-transparent plane at z = 0
    x = np.linspace(min(ship_x + torpedo_x), max(ship_x + torpedo_x), 50)
    y = np.linspace(min(ship_y + torpedo_y), max(ship_y + torpedo_y), 50)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)  # Plane at z = 0

    ax.plot_surface(X, Y, Z, color='c', alpha=0.5, rstride=100, cstride=100, label='Surface')

    ax.set_xlabel('X position (m)')
    ax.set_ylabel('Y position (m)')
    ax.set_zlabel('Z position (m)')
    ax.legend()
    ax.set_title('3D Torpedo Hit Simulation (Ship on Surface)')

    # Set equal aspect ratio for all axes
    max_range = np.array([max(ship_x+torpedo_x)-min(ship_x+torpedo_x),
                          max(ship_y+torpedo_y)-min(ship_y+torpedo_y),
                          max(torpedo_z)-min(torpedo_z)]).max() / 2.0
    mid_x = (max(ship_x+torpedo_x)+min(ship_x+torpedo_x)) * 0.5
    mid_y = (max(ship_y+torpedo_y)+min(ship_y+torpedo_y)) * 0.5
    mid_z = (max(torpedo_z)+min(torpedo_z)) * 0.5

    # Adjust z-limits to start at the initial z-coordinate of the torpedo
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(az, mid_z + max_range)  # Set lower bound of z to initial torpedo z position
    plt.show()

# Example usage
start1 = time.time()
torpedo_hit_3d(60, 70, 250, 500, -500)
end = time.time()
print(end-start1)
