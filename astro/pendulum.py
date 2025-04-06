import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import sin, cos, pi

g = 9.81
m = 2
l = 0.8
theta = pi+0.1
theta_dot = 0
dt = 0.00001
theta_two = lambda theta:-(g/l)*sin(theta)
theta_ls = [theta]
present = 0.01
save = 0.0001
N = 0.1

for step in range(int(100/dt)):
    temp = theta_two(theta) * dt - N * theta_dot * dt
    theta_dot += temp
    theta += theta_dot*dt
    if step/(int(100/dt)) >= save:
        theta_ls.append(theta)
        save+=0.0001
    if step/(int(100/dt)) > present:
        theta_ls.append(theta)
        print(f"{present=}")
        present+=0.01



x_ls = [l * sin(theta) for theta in theta_ls]
y_ls = [-l * cos(theta) for theta in theta_ls]

def update(frame):
    pen.set_xdata([x_ls[frame]])
    pen.set_ydata([y_ls[frame]])
    line.set_xdata((0,x_ls[frame]))
    line.set_ydata((0,y_ls[frame]))
    return pen, line

fig, ax = plt.subplots()
ax.scatter(0,0,c='k')

x_big = max(x_ls) if max(x_ls)>abs(min(x_ls)) else abs(min(x_ls))
y_big = max(y_ls) if max(y_ls)>abs(min(y_ls)) else abs(min(y_ls))
big = (x_big if x_big>y_big else y_big)*1.2
ax.set_ylim(bottom=-big,top = big)
ax.set_xlim(right=-big, left=big)

pen = ax.plot(x_ls[0],y_ls[0],marker='o')[0]
line = ax.plot((0,x_ls[0]),(0,y_ls[0]),marker='_')[0]


ani = animation.FuncAnimation(fig=fig,func = update,frames = len(x_ls), interval=100 ,repeat=False)

plt.show()
