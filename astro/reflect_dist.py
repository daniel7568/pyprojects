import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import linspace

def dist(x):
    return ((x-a1)**2+b1**2)**0.5+((a2-x)**2+b2**2)**0.5
def newX(x1,x2):
    x_middle = (x1+x2)/2
    if dist(x_middle)<dist(x2):
        return x1,x_middle
    else:
        return x_middle,x2
def update(frame):
    global x1,x2
    x1,x2 = newX(x1,x2)
    x1_plot.set_xdata([x1,x1])
    x2_plot.set_xdata([x2,x2])
    return x1_plot,x2_plot


a1 =2
b1 = 7
a2 = 5
b2 = 3

x1 = a1
x2 = a2

fig, ax = plt.subplots()
ax.scatter((a1,a2),(b1,b2))

x_ls = linspace(1,5,200)
y_ls = [dist(xi) for xi in x_ls]

x_best = (a1*b2 + a2*b1)/(b1+b2)
ax.plot((x_best,x_best),(0,max(y_ls)))

ax.plot(x_ls,y_ls)
x1_plot = ax.plot((a1,a1),(0,max(y_ls)))[0]
x2_plot = ax.plot((a2,a2),(0,max(y_ls)))[0]



ani = animation.FuncAnimation(fig=fig,func = update,frames = 100000, interval=1000)
plt.show()