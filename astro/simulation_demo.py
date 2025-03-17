import csv
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


dt = 0.00007
au = 149_597_870_700
time_length = int(((365*24*60*60)//dt)//50)
skip = 20000
present = 0.01

p1 = np.array([0,au/2])
v1 = np.array([29_783*3,0])
m1 = 1.9891*10**32

p2 = np.array([0,0])
v2 = np.array([0,0])
m2 = 1.9891*10**30


with open("path_data.csv",'w',newline='') as f:
    writer = csv.writer(f,delimiter=' ')
    writer.writerow(["x1","y1","x2","y2"])
#    for x1,y1,x2,y2 in zip(x1_ls,y1_ls,x2_ls,y2_ls):
#        writer.writerow([x1,y1,x2,y2])



    for step in range(time_length):
        p1, v1, p2, v2 = new_state(p1,v1,m1,p2,v2,m2,dt)
        if step % skip == 0:
            writer.writerow([p1[0],p1[1],p2[0],p2[1]])
        if step/time_length >= present:
            print(f"{present=}")
            present+=0.01



