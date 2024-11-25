import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
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
    for deg in np.linspace(np.pi, np.pi / 2, 100):
        missile_vel = np.array([0.1*np.cos(deg),0.1*np.sin(deg),0])
        missile_a = np.array([missile_a_mag*np.cos(deg),missile_a_mag*np.sin(deg),0])
        missile_x = lambda t: 0.5*missile_a[0]*(t-lunched_time)**2+missile_vel[0]*(t-lunched_time)+missile_pos[0]
        missile_y = lambda t: 0.5 * missile_a[1] * (t-lunched_time) ** 2 + missile_vel[1] * (t-lunched_time) + missile_pos[1]
        distance = lambda t: np.sqrt(
            (missile_x(t)-target_x(t))**2 + (missile_y(t)-target_y(t))**2)
        intercept_t = minimize_scalar(distance,bounds=(0,500), method='bounded')
        if intercept_t.x > 0 and missile_x(intercept_t.x)>0 and missile_y(intercept_t.x)>0 and 0<=intercept_t.fun<=1:
            return deg, missile_vel, missile_a, intercept_t.x, missile_x(intercept_t.x),missile_y(intercept_t.x)
    else:
        return None,None,None,None,None,None

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
                                deg, missile_vel,missile_a,hit_time,x,y = intercept_angle(
                                    a, missile_pos, normal_x_target_pos,
                                normal_y_target_pos, normal_t_target_pos,lunched_time=launched_time)
                                if deg is not None:
                                    break
                            else:
                                print("can't hit")
                except Warning:
                    pass

        elif deg is not None:
            missile_pos = missile_pos + missile_vel * dt + time_update
            missile_vel += missile_a * dt
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
plt.scatter(x_target_pos, y_target_pos,  label="Target Path",c=t_target_pos, cmap='inferno', s=5, norm=norm_global)
plt.scatter(x,y,c='k',label="hit point",s=30)
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.legend()
plt.colorbar(label='Time (s)')
plt.ylim(top = max(y_target_pos)+20,bottom=-20)
plt.xlim(left=-20)
plt.title("Target and Missile Trajectories")
plt.grid(True)
plt.show()
print(t)
