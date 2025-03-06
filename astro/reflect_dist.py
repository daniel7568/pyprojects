import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import linspace

def dist(x):
    return ((x-a1)**2+b1**2)**0.5+((a2-x)**2+b2**2)**0.5
def new(x1,x2):
    x_middle = (x1+x2)/2
    if dist(x_middle)<dist(x2):
        return x1,x_middle
    else:
        return x_middle,x2
def update(frame):


a1 = 1
b1 = 2
a2 = 5
b2 = 3
fig, ax = plt.subplots()
ax.scatter((a1,a2),(b1,b2))

x_ls = linspace(1,5,200)
y_ls = [dist(xi) for xi in x_ls]

ax.plot(x_ls,y_ls)
x1_plot = ax.plot((a1,a1),(0,max(y_ls)))
x1_plot = ax.plot((a2,a2),(0,max(y_ls)))