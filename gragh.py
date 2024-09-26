import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# First plot
d = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
t = [0.4, 1.45, 2.77, 4.55, 6.45, 7.18, 10.66, 12.6, 14.88, 16.34]

plt.figure(figsize=(10, 6))
plt.scatter(x=t, y=d)

polynomial = Polynomial.fit(t, d, 1)
line = polynomial(t)
plt.plot(t, line, color='red', label=f'Trend line: y={polynomial.coef[0]:.2f}x + {polynomial.coef[1]:.2f}')

plt.xlabel('Time (s)')
plt.ylabel('Distance (cm)')
plt.title('1 הלבט העובה יוסינ')
plt.legend()
plt.grid(True)
plt.show()

# Second plot
d2 = [13, 16, 19.5, 22, 26, 28.5, 32, 35, 38.5, 43.5]
t2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

plt.figure(figsize=(10, 6))
plt.scatter(x=t2, y=d2)

polynomial2 = Polynomial.fit(t2, d2, 1)
line2 = polynomial2(t2)
plt.plot(t2, line2, color='red', label=f'Trend line: y={polynomial2.coef[0]:.2f}x + {polynomial2.coef[1]:.2f}')

plt.xlabel('Time (s)')
plt.ylabel('Distance (cm)')
plt.title('הלבט העובה יוסינ 2')
plt.legend()
plt.grid(True)
plt.show()