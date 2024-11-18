import matplotlib.pyplot as plt
def hypotenuse_slope(f,x1,x2):
    return (f(x2)-f(x1))/(x2-x1)
def string_equation(f, x1, x2):
    m = hypotenuse_slope(f,x1,x2)
    return lambda x:m*x+f(x1)-x1*m
x = range(-10,11)
f = lambda x:x**2
fs = string_equation(f,3,7)
y = [f(x)for x in x]
ys = [fs(x)for x in x]
plt.plot(x,y)
plt.plot(x,ys)
plt.grid(True)
plt.show()


