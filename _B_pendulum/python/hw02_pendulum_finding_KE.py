#%%
import sympy as sp
from sympy.physics.vector import dynamicsymbols
from sympy.physics.vector.printing import vpprint, vlatex
from IPython.display import Math, display

#%%
####################################################################################
# example from Case Study B to find Kinetic Energy (with vectors/matrices)
####################################################################################
# importing these functions directly to make life a little easier and code a little more readable
from sympy import sin, cos, diff, Matrix, diag, symbols, Function, pretty_print, simplify, init_printing, latex
#init_printing(use_latex=True)

#defining mathematical variables (called symbols in sp) and time varying functions like z and theta
t, m1, m2, ell, g = symbols('t, m1, m2, ell, g')

z = dynamicsymbols('z')
theta = dynamicsymbols('theta')


#defining generalized coords and derivatives
q = Matrix([[z], [theta]])
qdot = q.diff(t)

#defining the kinetic energy
p1 = Matrix([[z+ell/2.0*sin(theta)], [ell/2.0*cos(theta)], [0]])
p2 = Matrix([[z], [0], [0]])

v1 = diff(p1, t)
v2 = diff(p2, t)

# by inspection, we can find the angular velocity of the rod
omega = Matrix([[0], [0], [theta.diff(t)]])

# if we are uncomfortable with the above, we can use the rotation matrix describing
# the orientation of the rod relative to the inertial frame to find the angular velocity
R = Matrix([[cos(theta), -sin(theta), 0], [sin(theta), cos(theta), 0], [0, 0, 1]])
#   Omeg_mat = R.diff(t)*R.T
#   omega = Omeg_mat.vee()

# next we define the inertia tensor for the rod
J = diag(0, m1*ell**2/12.0, m1*ell**2/12.0)


#%%
K = simplify(0.5*m1*v1.T@v1 + 0.5*m2*v2.T@v2 + 0.5*omega.T@R@J@R.T@omega)

# just grabbing the scalar inside this matrix so that we can do L = K-P, since P is a scalar
K = K[0,0]


#%%
display(Math(vlatex(K)))