import numpy as np
import control as cnt
from scipy import signal
import satelliteParam as P
P.Ts = 0.001  # sample time for simulation, this is necessary 
              # if our observer poles get too large in magnitude!


class ctrlLQR:
    def __init__(self):
        #--------------------------------------------------
        # LQR Control Design with integrator and observer
        #--------------------------------------------------
        # tuning parameters
        Q = np.diag([0.01, 100.0, 0.01, 5000.0, 1000.0])  # [theta, phi, theta_dot, phi_dot, e_phi_int]
        R = np.diag([0.5])  # [tau]

        # State Space Equations
        # xdot = A*x + B*u
        # y = C*x
        self.A = np.array([
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [-P.k / P.Js, P.k / P.Js, -P.b / P.Js, P.b / P.Js],
            [P.k / P.Jp, -P.k / P.Jp, P.b / P.Jp, -P.b / P.Jp]])
        self.B = np.array([[0.0],
                           [0.0],
                           [1.0 / P.Js],
                           [0.0]])
        self.C = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0]])

        # form augmented system
        Cr = np.array([[0.0, 1.0, 0.0, 0.0]])
        A1 = np.vstack((np.hstack((self.A, np.zeros((4,1)))), 
                        np.hstack((-Cr, np.zeros((1,1)))) ))
        B1 = np.vstack( (self.B, 0.0) )

        # Compute the gains if the system is controllable
        if np.linalg.matrix_rank(cnt.ctrb(A1, B1)) != 5:
            print("The system is not controllable")
        else:
            K1_lqr, _ , _ = cnt.lqr(A1, B1, Q, R)
            self.K = K1_lqr[:, 0:4]
            self.ki = K1_lqr[0, 4]

        # compute observer gains
        controller_eig = np.linalg.eig(A1 - B1 @ K1_lqr)
        des_obs_poles = np.ones(4) * np.real(np.min(controller_eig.eigenvalues)) * 10 + np.array([-0.2, -0.1, 0.1, 0.2])

        # Compute the gains if the system is observable
        if np.linalg.matrix_rank(cnt.ctrb(self.A.T, self.C.T)) != 4:
            print("The system is not observable")
        else:
            self.L = cnt.place(self.A.T, self.C.T, des_obs_poles).T

        # print gains to terminal
        print('K: ', self.K)
        print('ki: ', self.ki)
        print('L^T: ', self.L.T)

        #--------------------------------------------------
        # variables to implement integrator
        self.integrator_phi = 0.0  # integrator
        self.error_phi_d1 = 0.0  # error signal delayed by 1 sample
        # estimated state variables
        self.x_hat = np.array([
            [0.0],  # initial estimate for theta_hat
            [0.0],  # initial estimate for phi_hat
            [0.0],  # initial estimate for theta_hat_dot
            [0.0],  # initial estimate for phi_hat_dot
        ])
        self.tau_d1 = 0.0      # Computed torque delayed 1 sample

    def update(self, phi_r, y):
        # update the observer and extract z_hat
        x_hat = self.update_observer(y)
        phi_hat = x_hat[1, 0]
        
        # integrate error
        error_phi = phi_r - phi_hat
        self.integrator_phi = self.integrator_phi \
            + (P.Ts / 2.0) * (error_phi + self.error_phi_d1)
        self.error_phi_d1 = error_phi

        # Compute the state feedback controller
        tau_unsat = -self.K @ x_hat - self.ki * self.integrator_phi
        tau = saturate(tau_unsat[0,0], P.tau_max)
        self.tau_d1 = tau
        return tau, x_hat

    def update_observer(self, y_m):
        # update the observer using RK4 integration
        F1 = self.observer_f(self.x_hat, y_m)
        F2 = self.observer_f(self.x_hat + P.Ts / 2 * F1, y_m)
        F3 = self.observer_f(self.x_hat + P.Ts / 2 * F2, y_m)
        F4 = self.observer_f(self.x_hat + P.Ts * F3, y_m)
        self.x_hat = self.x_hat + P.Ts / 6 * (F1 + 2*F2 + 2*F3 + F4)
        return self.x_hat

    def observer_f(self, x_hat, y_m):
        # xhatdot = A*xhat + B*u + L(y-C*xhat)
        xhat_dot = self.A @ x_hat \
                   + self.B * self.tau_d1 \
                   + self.L @ (y_m - self.C @ x_hat)
        return xhat_dot


def saturate(u, limit):
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u

