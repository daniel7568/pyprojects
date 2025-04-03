import matplotlib.pyplot as plt

def calc_next_x(xn,f,dt):
    k1 = f(xn)*dt
    k2 = f(xn+0.5*k1)*dt
    k3 = f(xn + 0.5*k2)*dt
    k4 = f(xn + k3)*dt
    return xn + (1/6)*(k1+2*k2+2*k3+k4)

def clac_trajectory(x0,f,tf,dt):
    x_ls = [x0]
    t_ls = [0]
    for _ in range(int(tf/dt)):
        x_new = calc_next_x(x0,f,dt)
        x_ls.append(x_new)
        t_ls.append(t_ls[-1]+dt)
        x0 = x_new
    return t_ls,x_ls

def plot_trajectories()

x0 = 3
dt = 0.001
f = lambda x:x-x**2
duration = 100

t,x = clac_tragectory(x0,f,duration,dt)
plt.plot(t,x)
plt.plot
plt.show()