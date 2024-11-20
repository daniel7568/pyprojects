def create(n):
    return lambda a: a**n
p4 = create(4)
print(p4(2))
