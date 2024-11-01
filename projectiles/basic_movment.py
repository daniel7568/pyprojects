import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import square

target_pos = np.array([0,0.01])
target_vel = np.array([8.66,5])
missile_pos = np.array([8.66,5])
missile_vel = np.array([8.66,5])

grav = np.array([0,-9.81])
dt = 0.001

x_target_pos = [target_pos[0]]
y_target_pos = [target_pos[1]]

def relative_angle(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return np.atan2(dy, dx)
def calculate_new_cartesian_point(angle, vel):
    mag = square(vel[0]**2 + vel[1]**1)
    x =  mag * np.cos(angle)
    y =  mag * np.sin(angle)
    return np.array([x,y])




while target_pos[1]>0:
    target_pos = target_pos + target_vel*dt + 0.5*grav * dt**2
    target_vel = target_vel + grav*dt
    x_target_pos.append(target_pos[0])
    y_target_pos.append(target_pos[1])



    if np.hypot(target_pos[0] - missile_pos[0], target_pos[1] - missile_pos[1]) < 1:
        plt.scatter(missile_pos[0], missile_pos[1], c="r", label=f"Intersect")
        print(f"Hit at time: {seconds_to_hours(time)} ")
        break





plt.plot(x_pos,y_pos)
plt.show()
