import matplotlib.pyplot as plt
import numpy as np
x = np.arange(-20,21,0.1)
#print("enter a b and c and the power n")
#a = int(input("a:"))
#b = int(input("b:"))
#c = int(input("c:"))
#n = int(input("n:"))
#y = [a*x**n+b*x+c for x in x]
y = [np.cos(x) for x in x]
plt.plot(x,y)
plt.axhline(y=0 , color = 'k')
plt.axvline(x=0, color = 'k')
plt.grid(True)
plt.show()
