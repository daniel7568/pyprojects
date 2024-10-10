import matplotlib.pyplot as plt
x1=[0,2]
y1=[1,1]

x2=[2,4.5]
y2=[0,0]

x3=[4.5,6]
y3=[-2,-2]

plt.plot([-20,20],[0,0],"k")
plt.plot([0,0],[-20,20],"k")
plt.plot(x1,y1)
plt.plot(x2,y2)
plt.plot(x3,y3)
plt.grid(True)
plt.show()