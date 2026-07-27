#%%
from hw02_pendulum_finding_KE import *

#%%[markdown]
# The code imported from above shows how we defined q, q_dot, and necessary system parameters. Then we used position, velocity, and angular velocity to calculate kinetic energy.

#%%
#defining potential energy 
P = m1*g*ell/2.0*(cos(theta)-1)    #this is "mgh", where "h" is a function of generalized coordinate "q"

# can also do the following to get the same answer
#   g_vec = Matrix([[0], [g], [0]])  # defining gravity in the direction that increases potential energy
#   P = m1*g_vec.T@p1
#   P = P[0,0]


#calculate the lagrangian, using simplify intermittently can help the equations to be
#simpler, there are also options for factoring and grouping if you look at the sympy
#documentation.
L = simplify(K-P)

#%%
# Solution for Euler-Lagrange equations, but this does not include right-hand side (like friction and tau)
EL_case_studyB = simplify( diff(diff(L, qdot), t) - diff(L, q) )
#EL_case_studyB = simplify(L.diff(q_dot).diff(t) - L.diff(q))

display(Math(vlatex(EL_case_studyB)))



#%% 
############################################################
### Including friction and generalized forces, then solving for highest order derivatives
############################################################

# these are just convenience variables
zd = z.diff(t)
zdd = zd.diff(t)
thetad = theta.diff(t)
thetadd = thetad.diff(t)

# defining symbols for external force and friction
F, b = symbols('F, b')

# defining the right-hand side of the equation and combining it with E-L part
RHS = Matrix([[F - b*zd], [0]])
full_eom = EL_case_studyB - RHS

# finding and assigning zdd and thetadd
# if our eom were more complicated, we could rearrange, solve for the mass matrix, and invert it to move it to the other side and find qdd and thetadd
result = simplify(sp.solve(full_eom, (zdd, thetadd)))

#TODO - add an example of finding the same thing, but not using sp.solve


# result is a Python dictionary, we get to the entries we are interested in
# by using the name of the variable that we were solving for
zdd_eom = result[zdd]  # EOM for zdd, as a function of states and inputs
thetadd_eom = result[thetadd] # EOM for thetadd, as a function of states and inputs

display(Math(vlatex(zdd_eom)))
display(Math(vlatex(thetadd_eom)))


#%% [markdown]
# OK, now we can get the state variable form of the equations of motion.

#%%
import pendulumParam as P
import numpy as np

# defining fixed parameters that are not states or inputs (like g, ell, m1, m2, b)
# can be done like follows:
# params = [(m1, P.m1), (m2, P.m2), (ell, P.ell), (g, P.g), (b, P.b)]  

# but in this example, I want to keep the masses, length, and damping as variables so
# that I can simulate uncertainty in those parameters in real life. 
params = [(g, P.g)]


# substituting parameters into the equations of motion
zdd_eom = zdd_eom.subs(params)
thetadd_eom = thetadd_eom.subs(params)

# now defining the state variables that will be passed into f(x,u) 
state = np.array([z, theta, zd, thetad])
ctrl_input = np.array([F])

# defining the function that will be called to get the derivatives of the states
state_dot = np.array([zd, thetad, zdd_eom, thetadd_eom])


#%%
import numpy as np

# converting the function to a callable function that uses numpy to evaluate and 
# return a list of state derivatives
eom = sp.lambdify([state, ctrl_input, m1, m2, ell, b], state_dot, 'numpy')

# calling the function as a test to see if it works:
cur_state = np.array([0, 0, 0, 0])
cur_input = np.array([1])
print("x_dot = ", eom(cur_state, cur_input, P.m1, P.m2, P.ell, P.b))




#%% [markdown] 
# The next step is to save this function "f" so that we can use it with a numerical integrator, like 
# scipy.integrate.ivp.solve_ivp or the rk4 functions in the case studies. To save this function, we do the
# following:

#%%
import dill   # we may have to install dill using pip "python -m pip install dill"
dill.settings['recurse'] = True
dill.dump(eom, open("eom_case_study_B", "wb"))   #takes the function name "eom" and writes it to a file called "eom_case_study_B"


# we can then reload the function and test it again to make sure it works: 
eom_test = dill.load(open("eom_case_study_B", "rb"))

print("x_dot after reloading = ", eom_test(cur_state, cur_input, P.m1, P.m2, P.ell, P.b))
