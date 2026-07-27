#%%
from h3_generate_E_L import * 
from IPython.display import display, Math
from sympy.physics.vector import vlatex

#%%
# TODO - calculate the full equations of motion for the hummingbird, you can do this
# as a single equation = 0 (i.e. LHS - RHS), or you can treat each part individually and
# do the calculations for LHS and RHS separately. 

#%%[markdown]
# Longitudinal Dynamics are derived in this section: 

#%%
# step 0 - just print the equations for theta_ddot

#display(Math(vlatex(sp.expand_trig(LHS[1]))))
#display(Math(vlatex(sp.expand_trig(RHS[1]))))


#%%
# step 1 - substitute zero in for all the suggested variables

display('Longitudinal Dynamics (step 1):')
#display(Math(vlatex()))
#display(Math(vlatex()))

#%%

# step 2 - substitute F and Tau for f_l, f_r, and d*(f_l-f_r)

display('Longitudinal Dynamics (step 2):')
#display(Math(vlatex()))
#display(Math(vlatex()))

#%%
# step 3 - find the feedback linearization force F_fl
display('Feedback Linearization Force (step 3):')
#display(Math(vlatex(F_fl)))

#%%
# step 4 - find the linearized equation of motion for theta_ddot
display('Linearized Longitudinal Dynamics (step 4):')
#display(Math(vlatex(sp.Eq(theta.diff(t).diff(t), YOUR_RESULT_HERE))))


#%% [markdown]
# Lateral Dynamics are derived in this section:

#%%
# step 1 - substitute zero in for all the suggested variables
display('Lateral Dynamics (step 1):')
#display(Math(vlatex()))

#%%
# step 2 - find the equilibrium force F_e

#%%
# step 3 - find the equilibrium variables Tau_e and phi_e

#display(Math(vlatex()))
# by inspection Tau_e = 0, phi_e = 0 or pi, but 0 makes the most sense for the hb



#%%
# step 4 - find the linearized equation of motion for phi_ddot and psi_ddot

# HINT: I would suggest finding equations for phi_ddot and psi_ddot, then 
# you can linearize them like we have shown in the case studies using the 
# "jacobian" function, and substituting equilibrium values in. 

display('Linearized Lateral Dynamics (step 4): ')
#display(Math(vlatex(sp.simplify())))
#display(Math(vlatex(sp.simplify())))