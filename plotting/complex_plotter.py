import numpy as np
from mayavi import mlab
from sympy import symbols, lambdify

# Symbolic variable and function
x = symbols('x', real=True)
f = (1 - x**2)**0.5  # Mostly real, becomes complex outside [-1, 1]

# Use complex-safe math
f_lambdified = lambdify(x, f, modules=[{"sqrt": np.lib.scimath.sqrt}, "numpy"])

# Domain
x_vals = np.linspace(-3, 3, 500)

# Evaluate safely and force complex dtype
f_vals = np.array(f_lambdified(x_vals), dtype=complex)

# Separate components
real_vals = np.real(f_vals)
imag_vals = np.imag(f_vals)
abs_vals = np.abs(f_vals)

# --- Fix: remove NaNs that Mayavi can’t render ---
mask = np.isfinite(real_vals) & np.isfinite(imag_vals)
x_vals, real_vals, imag_vals, abs_vals = x_vals[mask], real_vals[mask], imag_vals[mask], abs_vals[mask]

# 3D Figure
mlab.figure('Complex Function Plot', bgcolor=(1, 1, 1), size=(900, 700))

# Plot the function: color by magnitude
mlab.plot3d(x_vals, real_vals, imag_vals, abs_vals, tube_radius=0.05, colormap='viridis')

# Axes and grid
axes = mlab.axes(
    xlabel='x (Real Input)',
    ylabel='Re(f(x))',
    zlabel='Im(f(x))',
    color=(0, 0, 0),
    line_width=1.0,
)
axes.label_text_property.color = (0, 0, 0)
axes.title_text_property.color = (0, 0, 0)

mlab.outline(color=(0.3, 0.3, 0.3), line_width=0.8)

# Colorbar and title
cb = mlab.colorbar(title='|f(x)|', orientation='vertical')
cb.title_text_property.color = (0, 0, 0)
cb.label_text_property.color = (0, 0, 0)

mlab.title('f(x) = sqrt(1 - x²)', height=0.9, size=0.5, color=(0, 0, 0))

# Camera view
mlab.view(azimuth=60, elevation=70, distance=8)

mlab.show()
