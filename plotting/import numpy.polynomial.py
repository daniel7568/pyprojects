import numpy as np
x = [0,0.6, 1.2, 1.8, 2.4, 3, 3.6, 4.2, 4.8, 5.4, 5.9 ]
t = [0, 1.63, 2.93, 4.55, 5.85, 7.54, 8.99, 9.89, 11.74, 13.21, 14.31]

coef = np.polyfit(t,x,1)
v = coef[0]
print(v)
print(coef)
