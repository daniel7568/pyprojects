import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

G = 6.6743*(10**-11)

def new_force_vectors(p1,m1,p2,m2):
    global G
    r = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5
    f1 = np.array([((G*m1*m2)/(r**3))*(p2[0]-p1[0]),((G*m1*m2)/(r**3))*(p2[1]-p1[1])])
    f2 = np.array([-f1[0],-f1[1]])
    return f1,f2

def new_state(p1,v1,m1,p2,v2,m2,dt):
     f1, f2 = new_force_vectors(p1,m1,p2,m2)
     a1 = np.array([f1[0] / m1, f1[1] / m1])
     a2 = np.array([f2[0] / m2, f2[1] / m2])
     v1 = v1 + a1 * dt
     v2 = v2 + a2 * dt
     p1 = p1 + v1*dt
     p2 = p2 + v2*dt
     return p1,v1,p2,v2

def update(frame):
    body1.set_xdata(x1_ls[:frame])
    body1.set_ydata(y1_ls[:frame])
    body2.set_xdata(x2_ls[:frame])
    body2.set_ydata(y2_ls[:frame])
    max_border = max(x1_ls[:frame+1]+ y1_ls[:frame+1])*1.2
    min_border = min(x1_ls[:frame+1] + y1_ls[:frame+1] + y2_ls[0])*1.2
    ax.set_xlim(left=min_border,right=max_border)
    ax.set_ylim(bottom=min_border,top=max_border)
    return body1,body2

dt = 1
au = 149_597_870_700
time_length = (3*365*24*60*60)//dt
skip = 5000

p1 = np.array([0,au])
v1 = np.array([29_783,0])
m1 = 5.97219*10**24
x1_ls = [p1[0]]
y1_ls = [p1[1]]

p2 = np.array([0,0])
v2 = np.array([0,0])
m2 = 1.9891*10**30
x2_ls = [p2[0]]
y2_ls = [p2[1]]

for step in range(time_length):
    p1, v1, p2, v2 = new_state(p1,v1,m1,p2,v2,m2,dt)
    if step % skip == 0:
        x1_ls.append(p1[0])
        y1_ls.append(p1[1])
        x2_ls.append(p2[0])
        y2_ls.append(p2[1])

fig, ax = plt.subplots()

body1 = ax.plot(x1_ls[0],y1_ls[0],marker='.')[0]
body2 = ax.plot(x2_ls[0],y2_ls[0],marker='.')[0]

ani = animation.FuncAnimation(fig=fig,func = update,frames = time_length, interval=0.00001)

plt.show()
