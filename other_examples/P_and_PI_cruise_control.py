#%%
import control as ctrl
from matplotlib import pyplot as plt

# %%
# define physical params of "model" for control design AND simulation
m = 1000.0 # kg - mass of car
b = 10.0 # N-s/m - damping due to wind, road friction, etc.
v_des = 20.0 # m-s

# define gains that are part of the controller, and will change the way 
# the system behaves
kp = 0 # proportional gain
ki = 0 # integral gain
u_cmd = v_des*b #open-loop command (see in-class calculation of this value)

# %%
# xfer function for nominal open-loop system
sys = ctrl.tf([u_cmd/m], [1, b/m])

# xfer function for closed-loop P control
sys_P_control = ctrl.tf([v_des*kp/m], [1, (kp+b)/m])

# xfer function for closed-loop PI control
sys_PI_control = ctrl.tf([v_des*kp/m, v_des*ki/m], [1, (b+kp)/m, ki/m])

# %%
print("roots of each system are:")
print("for open-loop:", ctrl.poles(sys))
print("for closed-loop with kp:", ctrl.poles(sys_P_control))
print("for closed-loop with kp and ki:", ctrl.poles(sys_PI_control))

# %%
# use toolbox functions to simulate step response (internally this is using
# numerical integration to simulate using the transfer function model that
# we provide. As long as the linear model is fairly accurate, this is an
# OK way to develop controllers (as opposed to numerically integrating
# the full state equations, which may be nonlinear or more complex).

t_sim = 200.0  # simulate for 200 seconds
t, v_nominal = ctrl.step_response(sys, t_sim)   # nominal response of the system to a step input 
t_P, v_P = ctrl.step_response(sys_P_control, t_sim) # response of system with P control to a step input in desired velocity
t_PI, v_PI = ctrl.step_response(sys_PI_control, t_sim) # response of system to PI control for a step input in desired velocity

# plotting the results
plt.figure()
plt.plot(t, v_nominal, t_P, v_P, t_PI, v_PI)
plt.legend(['nominal', 'P control', 'PI control'])
plt.xlabel('time (s)')
plt.ylabel('car velocity (m/s)')
plt.show()
# %%
