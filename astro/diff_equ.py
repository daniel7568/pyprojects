import matplotlib.pyplot as plt

def x_dot(x):
    return x-x**2

def calc_next_x(xn,dt):
    k1 = x_dot(xn)*dt
    k2 = x_dot(xn+0.5*k1)*dt
    k3 = x_dot(xn + 0.5*k2)*dt
    k4 = x_dot(xn + k3)*dt
    return xn + (1/6)*(k1+2*k2+2*k3+k4)

x0 = 1
x_ls = [x0]
t_ls = [0]
dt = 0.1