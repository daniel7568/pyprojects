from matplotlib import pyplot as plt
ax = plt.axes(projection = "3d")
ax.plot((0,0.433),(0,0.25),(0,0))
ax.plot((0,0.433),(0,0.25),(0,1))
plt.xlabel("X")
plt.ylabel("Y")
ax.set_zlabel("Z")
plt.show()

