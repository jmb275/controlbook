import numpy as np
import control as cnt
import armParam as P
P.Ts = 0.001  # sample time for simulation, this is necessary if our observer poles get too large in magnitude!


class ctrlLQR:
    def __init__(self):
        #--------------------------------------------------
        # LQR Control Design with integrator and observer
        #--------------------------------------------------
        #  tuning parameters
        Q = np.array([[100.0, 0.0, 0.0],   # theta
                      [0.0, 0.1, 0.0],   # theta_dot
                      [0.0, 0.0, 1000.0]])  # e_theta_int
        R = np.array([[5.0]])   # [tau]

        # State Space Equations
        # xdot = A*x + B*u
        # y_r = Cr*x
        self.A = np.array([[0.0, 1.0],
                          [0.0, -3.0 * P.b / P.m / (P.ell**2)]])
        self.B = np.array([[0.0],
                           [3.0 / P.m / (P.ell**2)]])        
        self.C = np.array([[1.0, 0.0]])

        # form augmented system
        Cr = self.C
        A1 = np.vstack((np.hstack((self.A, np.zeros((2,1)))), 
                        np.hstack((-Cr, np.zeros((1,1)))) ))
        B1 = np.vstack( (self.B, 0.0) )

        # Compute the gains if the system is controllable
        if np.linalg.matrix_rank(cnt.ctrb(A1, B1)) != 3:
            print("The system is not controllable")
        else:
            K1_lqr, _, _ = cnt.lqr(A1, B1, Q, R)
            self.K = K1_lqr[:, 0:2]
            self.ki = K1_lqr[0, 2]

        # observer design
        controller_eig = np.linalg.eig(A1 - B1 @ K1_lqr)
        des_obsv_poles = np.ones(2)*np.real(np.min(controller_eig.eigenvalues))*10 + np.array([0.1, -0.1])

        # Compute the gains if the system is observable
        Cm = self.C
        if np.linalg.matrix_rank(cnt.ctrb(self.A.T, self.C.T)) != 2:
            print("The system is not observerable")
        else:
            self.L = cnt.place(self.A.T, Cm.T, des_obsv_poles).T
        print('K: ', self.K)
        print('ki ', self.ki)
        print('L^T: ', self.L.T)

        #--------------------------------------------------
        # variables to implement integrator
        self.integrator = 0.0  # integrator
        self.error_prev = 0.0  # error signal delayed by 1 sample
        self.x_hat = np.array([
            [0.0],  # theta_hat_0
            [0.0],  # thetadot_hat_0
        ])
        self.tau_prev = 0.0  # control torque, delayed 1 sample

    def update(self, theta_r, y):
    #def update(self, theta_r, state):
        # update the observer and extract theta_hat
        x_hat = self.update_observer(y)
        theta_hat = x_hat[0, 0]
        # integrate error
        error = theta_r - theta_hat
        self.integrator = self.integrator \
                          + (P.Ts / 2.0) * (error + self.error_prev)
        self.error_prev = error

        # feedback linearizing torque tau_fl
        tau_fl = P.m * P.g * (P.ell / 2.0) * np.cos(theta_hat)

        # Compute the state feedback controller
        tau_tilde = -self.K @ x_hat - self.ki * self.integrator

        # compute total torque
        tau = saturate(tau_fl + tau_tilde[0, 0], P.tau_max)
        self.tau_prev = tau

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
        # compute feedback linearizing torque tau_fl
        theta_hat = x_hat[0, 0]
        tau_fl = P.m * P.g * (P.ell / 2.0) * np.cos(theta_hat)

        # xhatdot = A*(xhat-xe) + B*(u-ue) + L(y-C*xhat)
        xhat_dot = self.A @ x_hat\
                   + self.B * (self.tau_prev - tau_fl)\
                   + self.L * (y_m - self.C @ x_hat)
        return xhat_dot


def saturate(u, limit):
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u

