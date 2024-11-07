import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
t = list(range(0,65,5))
x =[0,0,100,300,700,1200,1900,2700,3700,5000,6300,7800,9200]

dt = [0]
dx = [0]
vel = [0]

for i in range(len(t)-1):
    dt.append(t[i+1]-t[i])
    dx.append(x[i+1]-x[i])
for i in range(len(t)-1):
    vel.append((x[i+1]-x[i])/(t[i+1]-t[i]))

coef = np.polyfit(t,x,2)
line_x = np.linspace(0,60,200)
line_y = np.polyval(coef,line_x)

table = pd.dataframe()
print(coef)
#plt.plot([-20,100],[0,0],"k",)
#plt.plot([0,0],[-20,100],"k")
#plt.scatter(t,x,label = "")
#plt.plot(line_x,line_y,label = f"speed is {coef[0]}")
#plt.plot(x2,y2,label = "ג")
#plt.plot(x3,y3,label = "ד")
plt.plot(t,vel)
plt.legend()
plt.grid(True)
plt.show()
