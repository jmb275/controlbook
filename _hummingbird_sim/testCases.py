errorTolerance = 0.001
dynamics_test_cases = [
# init_state (phi th, psi, phi_dot, th_dot, psi_dot),       input (pwm_left, pwm_right),        true state of plant (phi th, psi, phi_dot, th_dot, psi_dot) 
    ([[0.], [0.], [0.], [0.], [0.], [0.]],                  [[0.], [0.]],                       [[0.], [-0.00033088], [0.], [0.], [-0.06616823], [0.]]),
    ([[1.], [0.], [0.], [0.], [1.], [0.]],                  [[1.], [1.]],                       [[9.99996876e-01], [1.00216033e-02], [5.49387027e-04], [-2.30596331e-04], [1.00432053e+00], [1.09865283e-01]]),
    ([[0.], [1.], [0.], [0.], [0.], [1.]],                  [[100.], [-100.]],                  [[7.31654632e-02], [9.99800348e-01], [9.95134499e-03], [1.45018687e+01], [-4.01639444e-02], [9.86353614e-01]]),
    ([[0.], [0.], [1.], [0.], [-1.], [-1.]],                [[5.], [2.]],                       [[0.02199107], [-0.0080092], [0.99001172], [4.3592948], [-0.60175799], [-0.99604677]]),
    ([[1.], [0.], [0.], [1.], [0.], [-10.]],                [[-5.], [-2.]],                     [[9.88553674e-01], [-1.58600937e-03], [-1.01880917e-01], [-3.24348773e+00],[-3.18605188e-01], [-1.03759564e+01]]),
    ([[-1.], [-10.], [0.], [1.], [50.], [5.]],              [[0.5], [0.1]],                     [[-9.83592926e-01], [-9.49946956e+00], [4.55301806e-02], [2.39523860e+00],[ 5.00936012e+01], [4.30805861e+00]]),
    ([[0.], [5.], [-5.], [-5.], [5.], [-50.]],              [[-0.9], [-1.5]],                   [[-0.07064212], [5.0763994], [-5.47553565], [-9.69996898], [10.24893856], [-44.55460869]]),
    ([[1.], [2.], [3.], [4.], [5.], [6.]],                  [[-20.], [3.]],                     [[0.97876981], [2.0503235], [3.05911943], [-8.13224847], [5.06405749], [5.83277169]]),
    ([[-1.], [2.], [-3.], [4.], [-5.], [6.]],               [[5.], [5.]],                       [[-0.95579782], [1.95259208], [-2.93505771], [4.83014109], [-4.4735948], [6.9854602 ]]),
    ([[1.], [1.], [1.], [1.], [1.], [1.]],                  [[-2.], [-2.]],                     [[1.00861761], [1.00908968], [1.00861982], [0.72463434], [0.81866481], [0.72311757]])
]