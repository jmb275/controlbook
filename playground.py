# An empty file for experimenting with code.

#%%
import numpy as np
from control import *
from control.matlab import *
from sympy import *
import matplotlib.pyplot as plt
from sympy.physics.vector import dynamicsymbols
from sympy.physics.vector.printing import vlatex
from IPython.display import Math, display
#sin, cos, diff, Matrix, symbols, simplify, init_printing
init_printing()

# useful function to display sympy expressions in LaTeX format
def dotprint(expr):
    display(Math(vlatex(expr)))

# %% define symbols
m, l, J, t = symbols('m l J t')
theta = dynamicsymbols('theta')

# Define generalized coordinate
q = Matrix([[theta]])
qdot = diff(q, t)

# Define position
p = Matrix([[l/2*cos(theta)],
            [l/2*sin(theta)],
            [0]])


# velocity
v = diff(p, t)

dotprint(p)
dotprint(v)

# %% Rotational component
omega = Matrix([[0],
                [0],
                [diff(theta, t)]])
dotprint(omega)

# %% Kinetic energy
K = 1/2*m*(v.T*v) + 1/2*(omega.T*J*omega)
dotprint(K)
K = simplify(K[0])
dotprint(K)
K = simplify(K.subs('J', 1/12*m*l**2))
dotprint(K)

# %%
