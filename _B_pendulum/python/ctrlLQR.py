import numpy as np
from scipy import signal
import control as cnt
import pendulumParam as P
P.Ts = 0.001  # sample time for simulation, this is necessary if our observer poles get too large in magnitude!

class ctrlLQR:
    def __init__(self):
        #--------------------------------------------------
        # LQR Control Design with integrator and observer
        #--------------------------------------------------
        # tuning parameters
        Q = np.diag([30.0, 100.0, 1.0, 1.0, 1000.0])  # [z, theta, z_dot, theta_dot, e_z_int]
        R = np.diag([1.0])  # [F]   

        # State Space Equations
        # xdot = A*x + B*u
        # y = C*x
        self.A = np.array([
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, -3 * P.m1 * P.g / 4 / (.25 * P.m1 + P.m2),
                -P.b / (.25 * P.m1 + P.m2), 0.0],
            [0.0, 3*(P.m1 + P.m2)*P.g/2/(0.25*P.m1 + P.m2)/P.ell,
                3 * P.b / 2 / (.25 * P.m1 + P.m2) / P.ell, 0.0]])
        self.B = np.array([[0.0],
                           [0.0],
                           [1 / (.25 * P.m1 + P.m2)],
                           [-3.0 / 2 / (.25 * P.m1 + P.m2) / P.ell]])
        self.C = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0]])

        # form augmented system
        Cr = np.array([[1, 0]]) @ self.C
        A1 = np.concatenate((
                np.concatenate((self.A, np.zeros((4, 1))), axis=1),
                np.concatenate((-Cr, np.matrix([[0.0]])), axis=1)),
                axis=0)
        B1 = np.concatenate((self.B, np.matrix([[0.0]])), axis=0)

        # Compute the control gains if the system is controllable
        if np.linalg.matrix_rank(cnt.ctrb(A1, B1)) != 5:
            print("The system is not controllable")
        else:
            K1_lqr, _ , _ = cnt.lqr(A1, B1, Q, R)
            self.K = K1_lqr[:, 0:4]
            self.ki = K1_lqr[0, 4]
            
        # compute observer gains
        controller_eig = np.linalg.eig(A1 - B1 @ K1_lqr)
        des_obs_poles = np.ones(4) * np.real(np.min(controller_eig.eigenvalues)) * 10 + np.array([-0.2, -0.1, 0.1, 0.2])

        # Compute the observer gains if the system is observable
        if np.linalg.matrix_rank(cnt.ctrb(self.A.T, self.C.T)) != 4:
            print("The system is not observable")
        else:
            self.L = cnt.place(self.A.T, self.C.T, 
                                        des_obs_poles).T
        # print gains to terminal
        print('K: ', self.K)
        print('ki: ', self.ki)
        print('L^T: ', self.L.T)

        # variables to implement integrator
        self.integrator_z = 0.0  # integrator
        self.error_z_prev = 0.0  # error signal delayed by 1 sample
        # estimated state variables
        self.x_hat = np.array([
            [0.0],  # initial estimate for z_hat
            [0.0],  # initial estimate for theta_hat
            [0.0],  # initial estimate for z_hat_dot
            [0.0]])  # initial estimate for theta_hat_dot
        self.F_prev = 0.0  # Computed Force, delayed by one sample
        
    def update(self, z_r, y):
        # update the observer and extract z_hat
        x_hat = self.update_observer(y)
        z_hat = x_hat[0, 0]
        # integrate error
        error_z = z_r - z_hat
        self.integrator_z = self.integrator_z \
            + (P.Ts / 2.0) * (error_z + self.error_z_prev)
        self.error_z_prev = error_z
        # Compute the state feedback controller
        F_unsat = -self.K @ x_hat - self.ki * self.integrator_z
        F = saturate(F_unsat[0,0], P.F_max)
        self.F_prev = F
        return F, x_hat

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
                   + self.B * self.F_prev \
                   + self.L @ (y_m-self.C @ x_hat)
        return xhat_dot


def saturate(u, limit):
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u

