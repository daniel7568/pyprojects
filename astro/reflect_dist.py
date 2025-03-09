import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import linspace

def dist(x):
    return ((x-a1)**2+b1**2)**0.5+((a2-x)**2+b2**2)**0.5
def newX(x1,x2):
    if dist(x1)<dist(x2):
        return x1,(x1+x2)/2
    else:
        return (x1+x2)/2,x2
def update(frame):
    global x1,x2
    x1,x2 = newX(x1,x2)
    x1_plot.set_xdata([x1,x1])
    x2_plot.set_xdata([x2,x2])
    return x1_plot,x2_plot


a1 =2
b1 = 20
a2 = 5
b2 = 1

x1 = a1
x2 = a2

fig, ax = plt.subplots()
ax.scatter((a1,a2),(b1,b2),label="the 2 points")

x_ls = linspace(1,5,200)
y_ls = [dist(xi) for xi in x_ls]

x_best = (a1*b2 + a2*b1)/(b1+b2)
ax.plot((x_best,x_best),(0,max(y_ls)),label="the analytic solution")

ax.plot(x_ls,y_ls,label="the full distence of the reflection travel based on x value")
x1_plot = ax.plot((a1,a1),(0,max(y_ls)),label="right border of the numeric solution")[0]
x2_plot = ax.plot((a2,a2),(0,max(y_ls)),label="right border of the numeric solution")[0]

ani = animation.FuncAnimation(fig=fig,func = update,frames = 100, interval=1000)

plt.legend()
plt.show()