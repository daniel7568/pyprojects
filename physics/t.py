import matplotlib.pyplot as plt
x1= [0,30,40,60]
y1=[20,80,80,60]

x2=[0,10]
y2=[0,10]

x3=[0,1,2,3,4,5,6,7]
y3=[0,0.5,1,1.5,2.5,4,6,10]

plt.plot([-20,100],[0,0],"k",)
plt.plot([0,0],[-20,100],"k")
plt.plot(x1,y1,label = "")
#plt.plot(x2,y2,label = "ג")
#plt.plot(x3,y3,label = "ד")
plt.legend()
plt.grid(True)
plt.show()