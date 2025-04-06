import matplotlib.pyplot as plt
from math import e,sin

def calc_next_x(xn,f,dt):
    k1 = f(xn)*dt
    k2 = f(xn+0.5*k1)*dt
    k3 = f(xn + 0.5*k2)*dt
    k4 = f(xn + k3)*dt
    return xn + (1/6)*(k1+2*k2+2*k3+k4)

def calc_trajectory(x0,f,tf,dt):
    x_ls = [x0]
    t_ls = [0]
    for _ in range(int(tf/dt)):
        x_new = calc_next_x(x0,f,dt)
        x_ls.append(x_new)
        t_ls.append(t_ls[-1]+dt)
        x0 = x_new
    return t_ls,x_ls


def plot_trajectories(x_range,f,tf,dt):
    for xi in x_range:
        t,x = calc_trajectory(xi,f,tf,dt)
        plt.plot(t,x)
#    plt.show()


x_0 = 3
dt = 0.0001
f = lambda x:e**(-x)*sin(x)
duration = 6
ls = [i/4 for i in range(-45,21)]
plot_trajectories(ls,f,duration,dt)
plt.plot([0,1],[0,0],c='k',lw=1)
plt.show()