import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from matplotlib.colors import PowerNorm

target_pos = np.array([0, 0.01, 0])
target_vel = np.array([0.433, 0.25, 0])
missile_pos = np.array([2000, 0, 0])
missile_vel = np.array([0, 0, 0])
grav = np.array([0, -9.81, 0])

x_target_pos = [target_pos[0]]
y_target_pos = [target_pos[1]]
t_target_pos = [target_pos[2]]
normal_x_target_pos = []
normal_y_target_pos = []
normal_t_target_pos = []
x_missile_pos = []
y_missile_pos = []
t_missile_pos = []

t = 0
acurate_count = 0
dt = 0.001
pi = np.pi
time_update = np.array([0, 0, dt])
launched = False
hit = False
target_a = 20
terminal_speed = 200
deg = None
missile_a = 0

def intercept_angle(missile_a_mag,missile_pos,target_x,target_y,time,lunched_time):
    coef_x = np.polyfit(time,target_x,1)
    coef_y = np.polyfit(time, target_y,2)
    target_x = lambda t:coef_x[0]*t+coef_x[1]
    target_y = lambda t:coef_y[0]*t**2+coef_y[1]*t+coef_y[2]
    missile_x = lambda t,deg: 0.5 * missile_a_mag*np.cos(deg) * (t - lunched_time) ** 2 + missile_pos[0]
    missile_y = lambda t,deg: 0.5 * (missile_a_mag*np.sin(deg)-9.81) * (t - lunched_time) ** 2 + missile_pos[1]
    distance = lambda td: np.sqrt(
        (missile_x(td[0],td[1]) - target_x(td[0])) ** 2 + (missile_y(td[0],td[1]) - target_y(td[0])) ** 2)
    intercept = minimize(distance, x0 = np.array([15,np.pi/1.5]) , bounds=[(0, 30),(np.pi/2,np.pi)], method='L-BFGS-B',options={'maxiter': 1000})
    if missile_x(intercept.x[0],intercept.x[1]) > 0 and missile_y(
            intercept.x[0],intercept.x[1]) > 0 and 0 <= intercept.fun <= 1:
        print(f"intercept time is {intercept.x[0]}")
        print(f"intercept deg is {intercept.x[1]}")
        return intercept.x[1], missile_x(intercept.x[0],intercept.x[1]), missile_y(intercept.x[0],intercept.x[1])
    else:
        return None,None,None

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

            if len(normal_x_target_pos) > 5:
                try:
                    coef = np.polyfit(normal_x_target_pos, normal_y_target_pos, 2)
                    if coef[0] < 0:
                        acurate_count += 1
                        if acurate_count > 2:
                            launched = True
                            launched_time = t
                            missile_pos = missile_pos + np.array([0,0,launched_time])
                            time_to_max_speed = None
                            missile_a_vec = None

                            # Try different acceleration magnitudes
                            for a in range(60, 110):
                                deg,x,y = intercept_angle(
                                    a, missile_pos, normal_x_target_pos,
                                normal_y_target_pos, normal_t_target_pos,lunched_time=launched_time)
                                if deg is not None:
                                    missile_a = np.array([a*np.cos(deg),a*np.sin(deg)-9.81,0])
                                    break
                            else:
                                print("can't hit")
                except Warning:
                    pass

        elif deg is not None:
            missile_pos = missile_pos + missile_vel * dt + time_update
            missile_vel = missile_vel + missile_a * dt
            x_missile_pos.append(missile_pos[0])
            y_missile_pos.append(missile_pos[1])
            t_missile_pos.append(missile_pos[2])

    x_target_pos.append(target_pos[0])
    y_target_pos.append(target_pos[1])
    t_target_pos.append(target_pos[2])
    t += dt

norm_global = PowerNorm(gamma=1, vmin=0, vmax= max(t_target_pos))
plt.figure(figsize=(10, 6))
plt.scatter(x_missile_pos, y_missile_pos,  label="Missile Path", c=t_missile_pos, cmap='inferno', s=5, norm=norm_global)
p = plt.scatter(x_target_pos, y_target_pos,  label="Target Path",c=t_target_pos, cmap='inferno', s=5, norm=norm_global)
plt.scatter(x,y,c='k',label="hit point",s=30)
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.legend()
plt.colorbar(p,label='Time (s)')
plt.ylim(top = max(y_target_pos)+20,bottom=-20)
plt.xlim(left=-20)
plt.title("Target and Missile Trajectories")
plt.grid(True)
plt.show()
print(t)
