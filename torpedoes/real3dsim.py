import math
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)


def calculate_direction(p1, p2):
    return Vector3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z).normalize()


def torpedo_hit_3d(target_speed, torpedo_speed):
    dt = 0.01  # Time step
    max_time = 300  # Maximum simulation time

    # Random initial positions for the target object and torpedo in the range [-500, 500]
    target_pos = Vector3D(random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-1000, 1000))
    torpedo_pos = Vector3D(random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-1000, 1000))

    target_direction = Vector3D(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
    target_vel = target_direction * target_speed

    target_trajectory = [target_pos]
    torpedo_trajectory = [torpedo_pos]
    time = 0
    intersection_point = None

    while True:
        time += dt
        # Move target in a random direction in 3D space
        new_target_pos = target_pos + target_vel * dt
        target_pos = new_target_pos
        target_trajectory.append(target_pos)

        # Randomly change target direction occasionally
        if random.random() < 0.005:  # % chance each step
            new_direction = Vector3D(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            target_vel = new_direction * target_speed

        # Calculate torpedo direction and move toward the target
        torpedo_direction = calculate_direction(torpedo_pos, target_pos)
        torpedo_vel = torpedo_direction * torpedo_speed
        torpedo_pos = torpedo_pos + torpedo_vel * dt
        torpedo_trajectory.append(torpedo_pos)

        # Check for collision
        distance = (target_pos + torpedo_pos * -1).magnitude()
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

    target_x = [p.x for p in target_trajectory]
    target_y = [p.y for p in target_trajectory]
    target_z = [p.z for p in target_trajectory]
    torpedo_x = [p.x for p in torpedo_trajectory]
    torpedo_y = [p.y for p in torpedo_trajectory]
    torpedo_z = [p.z for p in torpedo_trajectory]

    ax.plot(target_x, target_y, target_z, label='Target Object', color='blue')
    ax.plot(torpedo_x, torpedo_y, torpedo_z, label='Torpedo', color='red')

    if intersection_point:
        ax.scatter([intersection_point.x], [intersection_point.y], [intersection_point.z],
                   color='green', s=100, label='Intersection')

    # Create a semi-transparent plane at z = 0
    x = np.linspace(min(target_x + torpedo_x), max(target_x + torpedo_x), 50)
    y = np.linspace(min(target_y + torpedo_y), max(target_y + torpedo_y), 50)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)  # Plane at z = 0

    #ax.plot_surface(X, Y, Z, color='gray', alpha=0.5, rstride=100, cstride=100, label='Surface')

    ax.set_xlabel('X position (m)')
    ax.set_ylabel('Y position (m)')
    ax.set_zlabel('Z position (m)')
    ax.legend()
    ax.set_title('3D Torpedo Hit Simulation (Freely Moving Object)')

    # Set equal aspect ratio for all axes
    max_range = np.array([max(target_x + torpedo_x) - min(target_x + torpedo_x),
                          max(target_y + torpedo_y) - min(target_y + torpedo_y),
                          max(target_z + torpedo_z) - min(target_z + torpedo_z)]).max() / 2.0
    mid_x = (max(target_x + torpedo_x) + min(target_x + torpedo_x)) * 0.5
    mid_y = (max(target_y + torpedo_y) + min(target_y + torpedo_y)) * 0.5
    mid_z = (max(target_z + torpedo_z) + min(target_z + torpedo_z)) * 0.5

    # Adjust z-limits to start at the initial z-coordinate of the torpedo
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    if min(torpedo_z)<min(target_z):
        ax.set_zlim(min(torpedo_z), mid_z + max_range)  # Set lower bound of z to initial torpedo z position
    else:
        ax.set_zlim(min(target_z), mid_z + max_range)
    plt.show()


# Example usage: randomly initialized target and torpedo positions
torpedo_hit_3d(70, 60)

