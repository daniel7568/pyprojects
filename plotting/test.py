import matplotlib.pyplot as plt
def f(x):
    return(x**2)
dx = 1
x = -20
while x <= 20:
    plt.scatter(x,f(x), c = "b")
    x += dx
plt.grid(True)
plt.show()
