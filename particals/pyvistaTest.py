import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.optimize import minimize
from matplotlib.colors import PowerNorm
import pyvista as pv

target_pos = np.array([0, 0.01, 0, 0])
target_vel = np.array([0.433, 0.25, 0.25, 0])
missile_pos = np.array([2000, 0, 1000, 0])
missile_vel = np.array([0, 0, 0, 0])
grav = np.array([0, -9.81, 0, 0])

x_target_pos = [target_pos[0]]
y_target_pos = [target_pos[1]]
z_target_pos = [target_pos[2]]
t_target_pos = [target_pos[3]]
normal_x_target_pos = []
normal_y_target_pos = []
normal_z_target_pos = []
normal_t_target_pos = []
x_missile_pos = []
y_missile_pos = []
z_missile_pos = []
t_missile_pos = []

t = 0
acurate_count = 0
dt = 0.01
pi = np.pi
time_update = np.array([0, 0, 0, dt])
launched = False
hit = False
target_a = 20
terminal_speed = 200
deg1 = None
missile_a = 0

def intercept_angle(missile_a_mag,missile_pos,target_x,target_y,target_z,time,lunched_time):
    coef_x = np.polyfit(time,target_x,1)
    coef_y = np.polyfit(time, target_y,2)
    coef_z = np.polyfit(time, target_z, 1)
    target_x = lambda t:coef_x[0]*t+coef_x[1]
    target_y = lambda t:coef_y[0]*t**2+coef_y[1]*t+coef_y[2]
    target_z = lambda t:coef_z[0]*t+coef_z[1]
    missile_x = lambda t, deg: 0.5 * missile_a_mag * np.cos(deg) * (t - lunched_time) ** 2 + missile_pos[0]
    missile_y = lambda t, deg: 0.5 * (missile_a_mag * np.sin(deg) - 9.81) * (t - lunched_time) ** 2 + missile_pos[1]
    missile_z = lambda t, deg: 0.5 * missile_a_mag * np.sin(deg) * (t - lunched_time) ** 2 + missile_pos[2]
    distance = lambda td: np.sqrt(
        (missile_x(td[0],td[1]) - target_x(td[0])) ** 2 + (missile_y(td[0],td[1]) - target_y(td[0])) ** 2 + (missile_z(td[0],td[2]) - target_z(td[0])) ** 2)
    intercept = minimize(distance, x0=np.array([15, np.pi / 1.5,np.pi/4]), bounds=[(0, 30), (np.pi / 2, np.pi),(-np.pi,np.pi)],
                         method='L-BFGS-B', options={'maxiter': 1000})
    if missile_x(intercept.x[0],intercept.x[1])>0 and missile_y(intercept.x[0],intercept.x[1])>0 and 0<=intercept.fun<=2:
        return intercept.x[1], intercept.x[2], missile_x(intercept.x[0],intercept.x[1]),missile_y(intercept.x[0],intercept.x[1]), missile_z(intercept.x[0],intercept.x[2])
    else:
        return None,None,None,None

v_angle_xy = np.arctan2(target_vel[1], target_vel[0])
v_angle_xz = np.arctan2(target_vel[2], target_vel[0])
a_vector = np.array([target_a * np.sin(v_angle_xy), target_a * np.cos(v_angle_xy), target_a*np.sin(v_angle_xz), 0])

while target_pos[1] > 0:
    target_pos +=  target_vel * dt + time_update
    target_vel = target_vel + (grav + a_vector if t<10 else grav) * dt
    if not launched and t>10:
        normal_x_target_pos.append(target_pos[0])
        normal_y_target_pos.append(target_pos[1])
        normal_z_target_pos.append(target_pos[2])
        normal_t_target_pos.append(target_pos[3])
        v_angle = np.arctan2(target_vel[1], target_vel[0])

        if len(normal_x_target_pos) > 5:
            try:
                coef = np.polyfit(normal_x_target_pos, normal_y_target_pos, 2)
                if coef[0] < 0:
                    acurate_count += 1
                    if acurate_count > 2:
                        launched = True
                        launched_time = t
                        missile_pos = missile_pos + np.array([0,0,0,launched_time])
                        time_to_max_speed = None
                        missile_a_vec = None

                        for a in range(110, 200):
                            deg1, deg2, x,y,z = intercept_angle(
                                a, missile_pos, normal_x_target_pos,normal_y_target_pos,
                            normal_z_target_pos, normal_t_target_pos,lunched_time=launched_time)
                            if deg1 is not None:
                                missile_a = np.array([a*np.cos(deg1),a*np.sin(deg1)-9.81,a*np.sin(deg2),0])
                                break
                        else:
                            print("can't hit")
            except Warning:
                pass
    elif deg1 is not None:
        missile_pos = missile_pos + missile_vel * dt + time_update
        missile_vel = missile_vel + missile_a * dt
        x_missile_pos.append(missile_pos[0])
        y_missile_pos.append(missile_pos[1])
        z_missile_pos.append(missile_pos[2])
        t_missile_pos.append(missile_pos[3])

    x_target_pos.append(target_pos[0])
    y_target_pos.append(target_pos[1])
    z_target_pos.append(target_pos[2])
    t_target_pos.append(target_pos[3])
    t += dt


target_points = np.column_stack((x_target_pos,y_target_pos,z_target_pos))
target_data = pv.PolyData(target_points)
missile_points = np.column_stack((x_missile_pos,y_missile_pos,z_missile_pos))
missile_data = pv.PolyData(missile_points)
plotter = pv.Plotter()
plotter.add_mesh(target_data,color='k')
plotter.add_mesh(missile_data,color='r')
plotter.show_grid()
plotter.add_floor().__doc__
plotter.show()


#fig = plt.figure()
#norm_global = PowerNorm(gamma=1, vmin=0, vmax= max(t_target_pos))
#ax = plt.axes(projection = "3d")
#ax.scatter(x_missile_pos, y_missile_pos, z_missile_pos,  label="Missile Path", c=t_missile_pos, cmap='inferno', s=5, norm=norm_global)
#p = ax.scatter(x_target_pos, y_target_pos, z_target_pos,  label="Target Path",c=t_target_pos, cmap='inferno', s=5, norm=norm_global)
#ax.scatter(x,y,z,c='k',label="hit point",s=30)
#plt.xlabel("X Position (m)")
#plt.ylabel("Y Position (m)")
#ax.legend()
#plt.ylim(top = max(y_target_pos)+20,bottom=-20)
#lt.xlim(left=-20)
#plt.title("Target and Missile Trajectories")
#fig.colorbar(p,label="time[s]")
#ax.grid(True)
#plt.show()
print(t)

