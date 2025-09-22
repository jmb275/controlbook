# run this file to test your vectors and matrices from the hummingbirdDynamics.py file
import numpy as np
from hummingbirdDynamics import HummingbirdDynamics as dynamics
import hummingbirdParam as P
import pickle as pkl

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
pickle_path = os.path.join(current_dir, 'test_matrices.pkl')
print(pickle_path)
print(f"Looking for file at: {pickle_path}")
print(f"File exists: {os.path.exists(pickle_path)}")
with open(pickle_path, 'rb') as f:
    data = pkl.load(f)

#data = pkl.load(open("./test_matrices.pkl", "rb"))
precision = 6

# states are defined in the following order: [phi, theta, psi, phi_dot, theta_dot, psi_dot]
states = [np.array([0, 0, 0, 0, 0, 0]).reshape(6, 1),
          np.array([0.1, 0.1, -0.1, 0.1, -0.1, 0.1]).reshape(6, 1),
          np.array([0.05, -0.3, 0.22, 0.2, 0.1, -0.1]).reshape(6, 1)]

# inputs are defined in the following order: [f_l, f_r]
inputs = [np.array([[0], [0]]),
          np.array([[0.1], [0.1]]),
          np.array([[0.05], [-0.05]])]
# the above doesn't match our tau
# force : float
#             force = (fl + fr). e.g. the second element of the tau matrix becomes
#             lT * force * cos(phi) using the above definition.
# torque : float
#             torque = d(fl - fr). e.g. the first element of teh tau matrix just
#             becomes torque, using the definition above.
inputs = [[inputs[0][0] + inputs[0][1], P.d*(inputs[0][0] - inputs[0][1])],
          [inputs[1][0] + inputs[1][1], P.d*(inputs[1][0] - inputs[1][1])],
          [inputs[2][0] + inputs[2][1], P.d*(inputs[2][0] - inputs[2][1])]]

hb_dynamics = dynamics(alpha=0.0)

def test_matrix(name, actual, expected):
    error = actual - expected
#    print(f"error: {error}")
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
    M_test = hb_dynamics._M(states[i])
    C_test = hb_dynamics._C(states[i])
    dP_dq_test = hb_dynamics._partialP(states[i])
    tau_test = hb_dynamics._tau(states[i], inputs[i][0][0], inputs[i][1][0])

    print(f"test {i+1}:")
    test_matrix("M", M_test, data['M'][i])
    test_matrix("C", C_test, data['C'][i])
    test_matrix("dP_dq", dP_dq_test, data['dP_dq'][i])
    test_matrix("tau", tau_test, data['tau'][i])
    print()
