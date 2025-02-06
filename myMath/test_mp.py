from mpmath import *
mp.dps = 5_000
f = lambda x:fdiv(1,fadd(1,power(x,2)))
res = quad(f,[0,1])
print(f"pi is {fmul(res,4)}")
