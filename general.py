# from itertools import groupby
#
#
# def getQuarter(point):
#     if point[0]>0 and point[1]>0:
#         return 1
#     elif point[0]>0 and point[1]<0:
#         return 2
#     elif point[0]<0 and point[1]>0:
#         return 4
#     elif point[0]<0 and point[1]<0:
#         return 3
#     return None
#
#
# def gruopyQuarters(ls):
#     group = groupby(ls, key=getQuarter)
#     return dict(group)
#
# points = [(2,5),(4,-5),(5,0),(-1,-1),(-4,3)]
# print(list(gruopyQuarters(points)[1]))

test = 14

n = 14
if 2<n<12:
    print(f"{n=}")