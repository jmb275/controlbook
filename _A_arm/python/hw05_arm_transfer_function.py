#%%
from hw06_arm_linearization import *
from sympy.physics.control import TransferFunction

# define 's' as symbolic variable for the Laplace domain
s = sp.symbols('s')
I = sp.eye(A_lin.shape[0])

#%%
# define C and D 
C = sp.Matrix([[1, 0]])
D = sp.Matrix([[0]])

# calc H(s) 
H = C @ (s*I - A_lin).inv() @ B_lin + D


H = sp.simplify(H)
display(Math(vlatex((sp.cancel(H[0,0])))))


#%%
# this is sufficient, but if we want to get the xfer function
# in a better form (monic form), we can do the following: 
# Separate numerator and denominator
num, den = H[0,0].as_numer_denom()

# Expand all paranetheses in denominator
expanded_den = sp.expand(den)

# Extract coefficient of highest-order term
order = sp.degree(expanded_den, s)
highest_order_term = expanded_den.coeff(s, order) #Extract the s^2 term

# Divide through by the highest_order_term
num_monic = sp.simplify(num/highest_order_term)
den_monic = sp.collect(sp.simplify(expanded_den/highest_order_term), s)

# we don't need this "TransferFunction" object, but it helps
# to print things properly without undoing the term rearrangement.
tf_monic = TransferFunction(num_monic, den_monic, s)
display(Math(vlatex((tf_monic))))

# %%
