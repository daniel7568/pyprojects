import matplotlib.pyplot as plt
from mpmath import *
mp.dps = 600

def home_C_dist(x, h=2):
    return sqrt(power(h,2)+power(x,2))
def farm_C_dist(x,d=4,H=3):
    return sqrt(fadd(power((fsub(d,x)),2),power(H,2)))
def min_dist(h,d,H,delta):
    dist = lambda x:fadd(home_C_dist(x,h),farm_C_dist(x,d,H))
    l = 0
    r = d
    while fabs(fsub(dist(r),dist(l)))>delta:
        new = dist(fdiv((fadd(l,r)),2))
        if dist(r)>new:
            r = fdiv(fadd(l,r),2)
        else:
            l = fdiv(fadd(l,r),2)
    return fdiv(fadd(l,r),2)
def min_x(h,d,H):
    return fdiv(fmul(d,h),fadd(h,H))

h = 3
d = 1
H = 4

lin = linspace(power(10,-100),1,100000)
x_best = min_x(h,d,H)
x_ls = [min_dist(h,d,H,delta) for delta in lin ]
print(lin)

plt.plot(lin,x_ls, label= "numeric")
plt.plot((0,1),(x_best,x_best),label = "analytic")
plt.legend()
plt.show()