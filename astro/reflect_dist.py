from math import sqrt
import matplotlib.pyplot as plt
from numpy import linspace
from mpmath import *

def home_C_dist(x, h=2):
    return sqrt(h**2+x**2)
def farm_C_dist(x,d=4,H=3):
    return sqrt((d-x)**2+H**2)
def min_dist(h,d,H,delta):
    dist = lambda x:home_C_dist(x,h)+farm_C_dist(x,d,H)
    l = 0
    r = d
    count=0
    while abs(dist(r)-dist(l))>delta:
        count += 1
        new = dist((l+r)/2)
        if dist(r)>new:
            r = (l+r)/2
        else:
            l = (l+r)/2
    return (l+r)/2
def min_x(h,d,H):
    return (d*h)/(h+H)

h = 3
d = 1
H = 4

x_best = min_x(h,d,H)
x_ls = [min_dist(h,d,H,delta) for delta in linspace(1,1e-30,10000)]

plt.plot(linspace(1,1e-30,10000),x_ls, label= "numeric")
plt.plot((0,1),(x_best,x_best),label = "analytic")
plt.legend()
plt.show()