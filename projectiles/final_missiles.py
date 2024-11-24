import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import solve
from typing import Tuple, Optional
import numpy.polynomial.polynomial as poly
from scipy.optimize import fsolve


from projectiles.basic_movment import intercept_times

# conditions and vectors
target_pos = np.array([0, 0.01, 0])
target_vel = np.array([0.433, 0.25, 0])
missile_pos = np.array([1000, 0, 0])
missile_vel = np.array([0, 0, 0])
grav = np.array([0, -9.81, 0])

# Lists
x_target_pos = [target_pos[0]]
y_target_pos = [target_pos[1]]
t_target_pos = [target_pos[2]]
normal_x_target_pos = []
normal_y_target_pos = []
normal_t_target_pos = []
x_missile_pos = []
y_missile_pos = []

# starting values
t = 0
acurate_count = 0
dt = 0.001
pi = np.pi
time_update = np.array([0, 0, dt])
launched = False
hit = False
target_a = 20
terminal_speed = 200



def intercept_angle(missile_a,missile_pos,target_x,target_y,time):
    coef_x = np.polyfit(time,target_x,1)
    coef_y = np.polyfit(time, target_y,2)
    target_x = lambda t:coef_x[0]*t+coef_x[1]
    target_y = lambda t:coef_y[0]*t**2+coef_y[1]*t+coef_y[2]
    for deg in np.arange(np.pi,np.pi/2,0.1):
        missile_vel = np.array([0.1*np.cos(deg),0.1*np.sin(deg),0])
        missile_a = np.array([missile_a*np.cos(deg),missile_a*np.sin(deg),0])
        missile_x = lambda t: 0.5*missile_a[0]*t**2+missile_vel[0]*t+missile_pos[0]
        missile_y = lambda t: 0.5 * missile_a[1] * t ** 2 + missile_vel[1] * t + missile_pos[1]
        final_x = lambda t: missile_x(t)-target_x(t)
        final_y = lambda t: missile_y(t)-target_y(t)
        intercept_t = fsolve((final_x,final_y),0)[0]
        if intercept_t > 0 and missile_x(intercept_t)>0 and missile_y(intercept_t)>0:
            return deg, missile_vel, missile_a


# Main simulation loop
while target_pos[1] > 0:
    target_pos +=  target_vel * dt + time_update
    if t < 10:
        v_angle = np.arctan2(target_vel[1], target_vel[0])
        a_vector = np.array([target_a * np.sin(v_angle), target_a * np.cos(v_angle), 0])
        target_vel = target_vel + grav * dt + a_vector * dt
    else:
        target_vel = target_vel + grav * dt
        if not launched:
            normal_x_target_pos.append(target_pos[0])
            normal_y_target_pos.append(target_pos[1])
            normal_t_target_pos.append(target_pos[2])
            v_angle = np.arctan2(target_vel[1], target_vel[0])

            # Only attempt polyfit if we have enough points
            if len(normal_x_target_pos) > 5:
                try:
                    coef = np.polyfit(normal_x_target_pos, normal_y_target_pos, 2)
                    if coef[0] < 0:
                        acurate_count += 1
                        if acurate_count > 2:
                            launched = True
                            launched_time = t
                            time_to_max_speed = None
                            missile_a_vec = None

                            # Try different acceleration magnitudes
                            for a in range(60, 110):
                                launch_angle = intercept_angle(
                                    missile_pos, a, terminal_speed,
                                    target_pos, target_vel, np.array([0, 0, 0]), grav
                                )
                                if launch_angle is not None:
                                    time_to_max_speed = terminal_speed / a
                                    missile_a_vec = np.array([
                                        a * np.cos(launch_angle),
                                        a * np.sin(launch_angle),
                                        0
                                    ])
                                    break

                            if time_to_max_speed is None:
                                print("Can't hit the target")
                                break  # Exit the main simulation loop
                except Warning:
                    pass  # Ignore warnings from polyfit

        elif missile_a_vec is not None:  # Only simulate missile if launch was successful
            missile_pos = missile_pos + missile_vel * dt + time_update
            if t - launched_time < time_to_max_speed:
                missile_vel = missile_vel + grav * dt + missile_a_vec * dt
            else:
                missile_vel = missile_vel + grav * dt
            x_missile_pos.append(missile_pos[0])
            y_missile_pos.append(missile_pos[1])

    x_target_pos.append(target_pos[0])
    y_target_pos.append(target_pos[1])
    t_target_pos.append(target_pos[2])
    t += dt

plt.figure(figsize=(10, 6))
if x_missile_pos:  # Only plot missile if it was launched
    plt.scatter(x_missile_pos, y_missile_pos, c="k", label="Missile Path", s=1)
plt.plot(x_target_pos, y_target_pos, 'r-', label="Target Path")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.legend()
plt.title("Target and Missile Trajectories")
plt.grid(True)
plt.show()