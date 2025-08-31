def getQuarter(p):
    if p[0] == 0 and p[1] == 0:
        return None
    elif p[0] > 0:
        if p[1] > 0:
            return 1
        else:
            return 2
    elif p[1] > 0:
        return 4
    return 3

def highish(ls):
    return max(ls, key=lambda x:x[1])

def QuatersCount(ls):
    quarters = {1:0, 2:0, 3:0, 4:0}
    for p in ls:
        q = getQuarter(p)
        if q is not None:
            quarters[q] += 1
    return quarters

def orderedQuarters(ls):
    qua
