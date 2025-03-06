import matplotlib.pyplot as plt
import matplotlib.animation as animation

def dist(x,a1,b1,a2,b2):
    return ((x-a1)**2+b1**2)**0.5+((a2-x)**2+b2**2)**0.5
def new(x1,x2):
    x_middle = (x1+x2)/2
    if dist(x_middle,a1,b1,a2,b2):

def update(frame):

