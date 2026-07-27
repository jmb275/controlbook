####################################################################################
# example from Case Study A to find Kinetic Energy (with vectors/matrices)
####################################################################################

# %%
import sympy as sp
from sympy.physics.vector import dynamicsymbols

# %%
# for pretty printing in Jupyter notebooks (doesn't work in terminal)
from sympy.physics.vector.printing import vlatex
from IPython.display import Math, display


def printsym(expr):
    """
    Renders latex from sympy expression when in a Jupyter-like environment. Does
    not print anything useful when running in a terminal. When in a terminal, use
    sp.pretty_print() instead.
    """
    display(Math(vlatex(expr)))


# %%
# Define regular symbols for time and all physical parameters
t, m, ell = sp.symbols("t, m, ell")

# Define dyanmicsymbols (time-varying symbols) for each generalized coordinate
theta = dynamicsymbols("theta")

# Form a matrix of the generalized coordinates
q = sp.Matrix([[theta]])

# Calculate the time derivative of the generalized coordinates
qdot = q.diff(t)

# %%
# To find KE, define position of the mass in the inertial frame

# NOTE: can do this, but using Rational will keep everything in fraction form
# p = Matrix([[1/2*ell*cos(theta)], [1/2*ell*sin(theta)], [0]])

# Rational keeps everything in fraction form
half = sp.Rational(1, 2)
p = sp.Matrix([[half * ell * sp.cos(theta)], [half * ell * sp.sin(theta)], [0]])

# %%
# Differentiate position to get velocity in the intertial frame
v = p.diff(t)

# %%
# Define the rotation matrix describing the orientation of the rod relative to the inertial frame
R = sp.Matrix(
    [[sp.cos(theta), -sp.sin(theta), 0], [sp.sin(theta), sp.cos(theta), 0], [0, 0, 1]]
)

# %%
# Find the angular velocity of the rod

# Method 1: note that rotation is solely about z-axis and write omega directly
omega = sp.Matrix([[0], [0], [theta.diff(t)]])

# Method 2: use rotation matrix to compute omega (this is a generic approach and will
# be used for lab, which is more complicated and this approach ends up being simpler)
Omega_mat = sp.trigsimp(R.diff(t) * R.T)

# Omega_mat is a skew-symmetric matrix, from which we can extract a 3-vector (omega)
omega = Omega_mat.vee()
# The following line is equivalent to calling vee():
# omega = sp.Matrix([[Omega_mat[2, 1]], [Omega_mat[0, 2]], [Omega_mat[1, 0]]])

# NOTE: if you inspect both methods, you will see that omega is the same

# %%
# Define the inertia tensor for the rod about its center of mass
# Jx: assuming a thin beam (no mass rotating at a distance from x-axis)
# Jy and Jz: table lookup for a beam gives 1/12*m*ell^2

# J = sp.diag(0, 1/12*m*ell**2, 1/12*m*ell**2) # may lead to floating point numbers
c = sp.Rational(1, 12)
J = sp.diag(0, c * m * ell**2, c * m * ell**2)

# %%
# Calculate the kinetic energy
# K = 1/2*m*v.T @ v + 1/2*omega.T @ R @ J @ R.T @ omega
K = half * m * v.T @ v + half * omega.T @ R @ J @ R.T @ omega
K = K[0, 0]
K = sp.trigsimp(K)

# %%
# Display the result
using_notebook = True  # set to False if running in terminal
if using_notebook:
    printsym(K)
else:
    sp.pretty_print(K)

# %%
