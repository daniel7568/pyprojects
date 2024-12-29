import  pyvista as pv
import numpy as np
p = np.random.uniform(low = -100, high = 100, size = (15,3))
print(p)
plotter = pv.Plotter()
poly = pv.PolyData(p)
plotter.add_mesh(poly, color = (27, 124, 242))
colors = np.array([(77, 148, 235),(125, 176, 240),(155, 194, 242),(191, 215, 245)])/255
for c in colors:
    p[:,0] -= 10
    poly = pv.PolyData(p)
    plotter.add_mesh(poly, color=c)
plotter.show()