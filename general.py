import matplotlib.pyplot as plt
import numpy as np

res = 50000
x = np.linspace(-2.5, 2.5, res)
N = 1000
b = 3
n = np.arange(N)[:, None]
print(n.shape)
print(x.shape)
mid = 0.55**n * np.cos(b**n*np.pi*x)
print(mid.shape)
y = np.sum(mid, axis=0)
plt.plot(x, y)
plt.show()