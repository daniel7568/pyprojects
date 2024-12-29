import  pyvista as pv
import numpy as np
p = np.random.uniform(low = -100, high = 100, size = (15,3))
print(p)
colors = [(27, 124, 242),(77, 148, 235),(125, 176, 240),(155, 194, 242),(191, 215, 245)]
poly = pv.PolyData(p)
plotter = pv.Plotter()
plotter.add_mesh(poly)
plotter.show()