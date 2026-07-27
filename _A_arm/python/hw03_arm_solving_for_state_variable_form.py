# %%
from hw02_arm_finding_KE import *

# %% [markdown]
# The code imported from above shows how we defined q, q_dot, and necessary system parameters.
# Then we used position, velocity, and angular velocity to calculate kinetic energy.

# %%
# Define potential energy
g = sp.symbols('g')

# This is "mgh", where "h" is a function of generalized coordinate "q"
# P =  m * g * ell / 2 * sp.sin(theta)
P =  half * m * g * ell * sp.sin(theta)

# Can also do the following to get the same answer:
#   g_vec = Matrix([[0], [g], [0]])  # defining gravity in the direction that increases potential energy
#   p1 = Matrix([[ell/2*cos(theta)], [ell/2*sin(theta)], [0]])
#   P = m*g_vec.T@p1
#   P = P[0,0]

# %%
# Calculate the lagrangian, using simplify intermittently can help the equations to be
# simpler, there are also options for factoring and grouping if you look at the sympy
# documentation.
L = K - P
# L = sp.simplify(K - P) # look at output before simplifying - not needed here

# %%
# Solution for Euler-Lagrange equations, but this does not include right-hand side (like friction and tau)
EL_case_studyA = sp.diff(sp.diff(L, qdot), t) - sp.diff(L, q)
# EL_case_studyA = sp.simplify(EL_case_studyA) # not needed here

printsym(EL_case_studyA)


# %%
############################################################
### Including friction and generalized forces, then solving for highest order derivatives
############################################################

# These are just convenience variables
thetad = theta.diff(t)
thetadd = thetad.diff(t)

# Defining symbols for external force and friction
tau, b = sp.symbols('tau, b')

# Defining the right-hand side of the equation and combining it with E-L part
RHS = sp.Matrix([[tau - b*thetad]])
full_eom = EL_case_studyA - RHS

# Finding and assigning zdd and thetadd
# If our eom were more complicated, we could rearrange, solve for the mass matrix, and invert it to move it to the other side and find qdd and thetadd
result = sp.solve(full_eom, (thetadd))

# %%
# TODO: - add an example of finding the same thing, but not using sp.solve

# Still uses sp.solve, but creates an equation and solves it
eom_eq = sp.Eq(EL_case_studyA, RHS)
result = sp.solve(eom_eq, thetadd)

# result is a Python dictionary, we get to the entries we are interested in
# by using the name of the variable that we were solving for
thetadd_eom = result[thetadd] # EOM for thetadd, as a function of states and inputs

printsym(thetadd_eom)


# %% [markdown]
# OK, now we can get the state variable form of the equations of motion.

# %%
import armParam as P
import numpy as np

# Defining fixed parameters that are not states or inputs (like g, ell, m, b)
# can be done like follows:
# params = [(m, P.m), (ell, P.ell), (g, P.g), (b, P.b)]

# But in this example, I want to keep the masses, length, and damping as variables so
# that I can simulate uncertainty in those parameters in real life.
params = {g: P.g}

# Substituting parameters into the equations of motion
# thetadd_eom = thetadd_eom.subs(params)

# Now defining the state variables that will be passed into f(x,u)
state = sp.Matrix([theta, thetad])
ctrl_input = sp.Matrix([tau])

# Defining the function that will be called to get the derivatives of the states
state_dot = sp.Matrix([thetad, thetadd_eom])


# %%
import numpy as np

# Converting the function to a callable function that uses numpy to evaluate and
# return a list of state derivatives
eom = sp.lambdify((state, ctrl_input, m, ell, b, g), state_dot, 'numpy')


# calling the function as a test to see if it works:
cur_state = np.array([0, 0])
cur_input = np.array([1])
print("x_dot = ", eom(cur_state, cur_input, P.m, P.ell, P.b, P.g))


# %% [markdown]
# The next step is to save this function "f" so that we can use it with a numerical integrator, like
# scipy.integrate.ivp.solve_ivp or the rk4 functions in the case studies. To save this function, we do the
# following:

# # Method 1
# Save function to a binary (non-readable) file
# %%
import dill   # we may have to install dill using pip "python -m pip install dill"
dill.settings['recurse'] = True

filename = "eom_case_study_A.pkl"  # use .pkl extension for dill files
with open(filename, "wb") as file_to_generate:
    dill.dump(eom, file_to_generate)   #takes the function name "eom" and writes it to a file called "eom_case_study_B"


# %%
# We can then reload the function and test it again to make sure it works (this
# would happen in your dynamics file, but we are showing an example of how to
# load the eom function that we saved to a file):
with open(filename, "rb") as generated_file:
    eom_test = dill.load(generated_file)

print("x_dot after reloading = ", eom_test(cur_state, cur_input, P.m, P.ell, P.b, P.g))

# %% [markdown]
# # Method 2
# Generate a python file from lambdified function

# %%
import inspect
import re

# When generating python source code, dynamicsymbols will show up as _Dummy_XX,
# so if we substitute the dynamic symbols with regular symbols first, the
# generated code will be easier to read. It will still create _Dummy_XX variables
# for inputs that are Matrix/array types, but the end result will be easier to read.
theta_sym, thetadot_sym = sp.symbols('theta thetadot')
q_sym = {theta: theta_sym, thetad: thetadot_sym}
state_sym = state.subs(q_sym)
state_dot_sym = state_dot.subs(q_sym)
# ctrl_input in this case was not created from dynamicsymbols, so no need to substitute

# %%
eom = sp.lambdify((state_sym, ctrl_input, m, ell, b, g), state_dot_sym, 'numpy')

# Function to replace dummy variables with x and u
def replace_dummy_vars(expr) -> str:
    # Extract first two dummy variables from function def line
    match = re.search(r'def _lambdifygenerated\(\s*(\S+),\s*(\S+),', expr)
    if not match:
        return expr  # No match found, return original expression
    dummy_1, dummy_2 = match.group(1), match.group(2)
    # Replace all occurrences of dummy_1 and dummy_2 in the entire string
    pattern = re.compile(r'\b(' + re.escape(dummy_1) + r'|' + re.escape(dummy_2) + r')\b')
    def replacement(m):
        return 'x' if m.group(0) == dummy_1 else 'u'
    result = pattern.sub(replacement, expr)
    return result

raw_source_code = inspect.getsource(eom)
# NOTE: raw_source_code breaks because it uses "array" rather than "np.array"

# You could change the import to be "from numpy import array, sin, cos", but I
# prefer to keep them namespaced to not mix them up with sympy.sin, etc., so the
# following lines make substitions for the whole file
source_code = re.sub('array', 'np.array', raw_source_code)
source_code = re.sub('cos', 'np.cos', source_code)
source_code = re.sub('sin', 'np.sin', source_code)
source_code = replace_dummy_vars(source_code)
source_code = re.sub('_lambdifygenerated', 'eom', source_code)
# label output as xdot rather than just return it
source_code = re.sub('return', 'xdot =', source_code)
source_code += '    return xdot.reshape(-1, 1)\n'

# Actually write the source code to a file
filename = "eom_generated.py"
with open(filename, "w") as file_to_write:
    file_to_write.write("import numpy as np\n\n\n")

    # Include these if you want to see the raw generated code in the file
    print("This is the raw generated source code from sympy/lambdify:")
    print(raw_source_code)
    # file_to_write.write("# This is the raw generated source code from sympy/lambdify\n")
    # file_to_write.write(raw_source_code)
    # file_to_write.write("\n\n")

    # This is the cleaned up version that is easier to read
    file_to_write.write("# This is the generated source code after some substitutions\n")
    file_to_write.write(source_code)

# %%
# We can then import the function and test it again to make sure it works (this
# would happen in your dynamics file, but we are showing an example of how to
# load the eom function that we saved to a file):
from eom_generated import eom as arm_eom

xdot_result = arm_eom(cur_state[:,None], cur_input[:,None], P.m, P.ell, P.b, P.g)
print("imported xdot = ", xdot_result)
print("xdot shape = ", xdot_result.shape)

# %%
