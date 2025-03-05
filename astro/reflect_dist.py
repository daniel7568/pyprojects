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

h = 7
d = 18
H = 5

lin = linspace(power(10,-100),1,100000)
x_best = min_x(h,d,H)
x_ls = [min_dist(h,d,H,delta) for delta in lin ]

print(f"analytic {home_C_dist(x_best,h)+farm_C_dist(x_best,d,H)}")
print(f"numeric {home_C_dist(x_ls[-1],h)+farm_C_dist(x_ls[-1],d,H)}")

plt.plot(lin,x_ls, label= "numeric")
plt.plot((0,1),(x_best,x_best),label = "analytic")
plt.legend()
plt.show()

def home_C_dist(x, a,b):
    return sqrt(fadd(power(b,2),power(fsub(x,a),2)))
def farm_C_dist(x,c,d):
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