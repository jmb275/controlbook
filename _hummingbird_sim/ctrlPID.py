import numpy as np
import hummingbirdParam as P


class ctrlPID:
    def __init__(self):
        # tuning parameters
        tr_pitch =
        zeta_pitch =
        self.ki_pitch =
        tr_yaw =
        zeta_yaw =
        self.ki_yaw =
        M =   # bandwidth separation between inner (roll) and outer (yaw) loops
        tr_roll =
        zeta_roll =
        # gain calculation
        b_theta = P.ellT/(P.m1 * P.ell1**2 + P.m2 * P.ell2**2 + P.J1y + P.J2y)
        b_psi =   # see eqn 5.4 in the hummingbird manual
        wn_pitch =
        wn_yaw =
        wn_roll =
        self.kp_pitch =
        self.kd_pitch =
        self.kp_roll =
        self.kd_roll =
        self.kp_yaw =
        self.kd_yaw =
        # print gains to terminal
        print('kp_pitch: ', self.kp_pitch)
        print('ki_pitch: ', self.ki_pitch)
        print('kd_pitch: ', self.kd_pitch)
        print('kp_roll: ', self.kp_roll)
        print('kd_roll: ', self.kd_roll)
        print('kp_yaw: ', self.kp_yaw)
        print('ki_yaw: ', self.ki_yaw)
        print('kd_yaw: ', self.kd_yaw)
        # sample rate of the controller
        self.Ts = P.Ts
        # dirty derivative parameters
        sigma = 0.05  # cutoff freq for dirty derivative
        self.beta = (2 * sigma - self.Ts) / (2 * sigma + self.Ts)
        # delayed variables
        self.phi_d1 = 0.
        self.phi_dot = 0.
        self.theta_d1 = 0.
        self.theta_dot = 0.
        self.psi_d1 = 0.
        self.psi_dot = 0.
        self.integrator_theta = 0.
        self.integrator_psi = 0.
        self.error_theta_d1 = 0.  # pitch error delayed by 1
        self.error_psi_d1 = 0.  # yaw error delayed by 1

    def update(self, r: np.ndarray, y: np.ndarray):
        theta_ref = r[0, 0]
        psi_ref = r[1, 0]
        phi = y[0, 0]
        theta = y[1, 0]
        psi = y[2, 0]
        force_equilibrium =
        # compute errors
        error_theta =
        error_psi =

        # update differentiators
        self.phi_dot =
        self.theta_dot =
        self.psi_dot =

        # update integrators
        self.integrator_theta =
        self.integrator_psi =

        # pitch control
        force_unsat =
        force = saturate(force_unsat, -P.force_max, P.force_max)

        # outer loop yaw control
        phi_ref_unsat =
        phi_ref = saturate(phi_ref_unsat, -np.pi/4, np.pi/4)

        # inner loop roll control
        error_phi =
        torque_unsat =
        torque = saturate(torque_unsat, -P.torque_max, P.torque_max)
        # convert force and torque to pwm signals
        pwm = np.array([[force + torque / P.d],               # u_left
                      [force - torque / P.d]]) / (2 * P.km)   # u_right
        pwm = saturate(pwm, 0, 1)
        # update all delayed variables
        self.phi_d1 = phi
        self.theta_d1 = theta
        self.psi_d1 = psi
        self.error_theta_d1 = error_theta
        self.error_psi_d1 = error_psi
        # return pwm plus reference signals
        return pwm, np.array([[phi_ref], [theta_ref], [psi_ref]])


def saturate(u, low_limit, up_limit):
    if isinstance(u, float) is True:
        if u > up_limit:
            u = up_limit
        if u < low_limit:
            u = low_limit
    else:
        for i in range(0, u.shape[0]):
            if u[i, 0] > up_limit:
                u[i, 0] = up_limit
            if u[i, 0] < low_limit:
                u[i, 0] = low_limit
    return u
