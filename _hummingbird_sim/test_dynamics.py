# run this file to test your vectors and matrices from the hummingbirdDynamics.py file
import numpy as np
from hummingbirdDynamics import HummingbirdDynamics as dynamics
import hummingbirdParam as P
import pickle as pkl
import os

# load the test matrices relative to this file so the test works
# regardless of the directory it is run from
current_dir = os.path.dirname(os.path.abspath(__file__))
pickle_path = os.path.join(current_dir, 'test_matrices.pkl')
with open(pickle_path, 'rb') as f:
    data = pkl.load(f)
precision = 6

# states are defined in the following order: [phi, theta, psi, phi_dot, theta_dot, psi_dot]
states = [np.array([0, 0, 0, 0, 0, 0]).reshape(6, 1),
          np.array([0.1, 0.1, -0.1, 0.1, -0.1, 0.1]).reshape(6, 1),
          np.array([0.05, -0.3, 0.22, 0.2, 0.1, -0.1]).reshape(6, 1)]

# inputs are defined in the following order: [f_l, f_r]
inputs = [np.array([[0], [0]]),
          np.array([[0.1], [0.1]]),
          np.array([[0.05], [-0.05]])]

hb_dynamics = dynamics(alpha=0.0)

def test_matrix(name, actual, expected):
    error = actual - expected
    correct_indices = np.abs(error) < 1e-14
    if correct_indices.all():
        print(f"{name:>10}: PASS")
    else:
        incorrect_indices = np.argwhere(~correct_indices)
        print(f"{name:>10}: FAIL")
        for r,c in incorrect_indices:
            print(f'{name:>20}[{r},{c}]: ', end='')
            print(f'yours = {actual[r,c]:<{precision+9}.{precision}g} ', end='')
            print(f'expected = {expected[r,c]:.{precision}g}')

for i in range(len(states)):
    M_test = hb_dynamics.M(states[i], hb_dynamics.param_vals)
    C_test = hb_dynamics.C(states[i], hb_dynamics.param_vals)
    dP_dq_test = hb_dynamics.dP_dq(states[i], hb_dynamics.param_vals)
    tau_test = hb_dynamics.tau(states[i], inputs[i], hb_dynamics.param_vals)

    print(f"test {i+1}:")
    test_matrix("M", M_test, data['M'][i])
    test_matrix("C", C_test, data['C'][i])
    test_matrix("dP_dq", dP_dq_test, data['dP_dq'][i])
    test_matrix("tau", tau_test, data['tau'][i])
    print()
