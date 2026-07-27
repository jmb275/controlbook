import numpy as np
import hummingbirdParam as P

# can use the following if you saved numpy versions of your SymPy functions
# import dill
# dill.settings['recurse'] = True


class HummingbirdDynamics:
    def __init__(self, alpha=0.0):
        # Initial state conditions
        self.state = np.array([
            [P.phi0],  # roll angle
            [P.theta0],  # pitch angle
            [P.psi0],  # yaw angle
            [P.phidot0],  # roll rate
            [P.thetadot0],  # pitch rate
            [P.psidot0],  # yaw rate
        ])

        # vary the actual physical parameters
        self.ell1 = P.ell1 * (1.+alpha*(2.*np.random.rand()-1.))
        self.ell2 = P.ell2 * (1.+alpha*(2.*np.random.rand()-1.))
        self.ell3x = P.ell3x * (1.+alpha*(2.*np.random.rand()-1.))
        self.ell3y = P.ell3y * (1.+alpha*(2.*np.random.rand()-1.))
        self.ell3z = P.ell3z * (1.+alpha*(2.*np.random.rand()-1.))
        self.ellT = P.ellT * (1.+alpha*(2.*np.random.rand()-1.))
        self.d = P.d * (1.+alpha*(2.*np.random.rand()-1.))
        self.m1 = P.m1 * (1.+alpha*(2.*np.random.rand()-1.))
        self.m2 = P.m2 * (1.+alpha*(2.*np.random.rand()-1.))
        self.m3 = P.m3 * (1.+alpha*(2.*np.random.rand()-1.))
        self.J1x = P.J1x * (1.+alpha*(2.*np.random.rand()-1.))
        self.J1y = P.J1y * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J1z = P.J1z * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J2x = P.J2x * (1.+alpha*(2.*np.random.rand()-1.))
        self.J2y = P.J2y * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J2z = P.J2z * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J3x = P.J3x * (1.+alpha*(2.*np.random.rand()-1.))
        self.J3y = P.J3y * (1. + alpha * (2. * np.random.rand() - 1.))
        self.J3z = P.J3z * (1. + alpha * (2. * np.random.rand() - 1.))
        self.km = P.km * (1. + alpha * (2. * np.random.rand() - 1.))
        self.beta = 0.001 # friction coefficient from lab manual

        # store the parameters in a list for easy access
        self.param_vals = [self.m1, self.m2, self.m3,
                           self.J1x, self.J1y, self.J1z,
                           self.J2x, self.J2y, self.J2z,
                           self.J3x, self.J3y, self.J3z,
                           self.ell1, self.ell2, self.ell3x,
                           self.ell3y, self.ell3z, self.ellT, self.d]

        # if you used the 'h3_generate_E-L.py" file to generate the functions,
        # and you saved them using dill, you can load them here
        #   self.M_func = dill.load(open("hb_M_func.pkl", "rb"))
        #   self.C_func = dill.load(open("hb_C_func.pkl", "rb"))
        #   self.dP_dq_func = dill.load(open("hb_dP_dq_func.pkl", "rb"))
        #   self.tau_func = dill.load(open("hb_tau_func.pkl", "rb"))
        # Once loaded, youc an also use them in the self.M, self.C, self.dP_dq, and self.tau function
        # definitions below.

        self.B = #TODO define the friction-based matrix of coefficients


    def update(self, u: np.ndarray):
        # This is the external method that takes the input u at time
        # t and returns the output y at time t.
        # later, we'll add a function to saturate the input forces
        self.rk4_step(u)  # propagate the state by one time sample
        y = self.h()  # return the corresponding output
        return y

    def f(self, state: np.ndarray, u: np.ndarray):
        # Return xdot = f(x,u)
        phidot = state[3, 0]
        thetadot = state[4, 0]
        psidot = state[5, 0]

        # TODO fill out the equations for each of the following in their
        # definitions below.
        M = self.M(state)
        C = self.C(state)
        dP_dq = self.dP_dq(state)
        tau = self.tau(state, u)

        # TODO write an expression for qddot from the lab manual equations,
        # remember that it will be in terms of M, C, dP_dq, -Bqdot, and tau
        # (but all of them will be numerical values, not functions)
        qddot =

        # define the second derivatives from qddot
        phiddot = qddot[0, 0]
        thetaddot = qddot[1, 0]
        psiddot = qddot[2, 0]

        # build xdot and return it
        xdot = np.array([[phidot],
                         [thetadot],
                         [psidot],
                         [phiddot],
                         [thetaddot],
                         [psiddot]])
        return xdot

    def h(self):
        # TODO Fill in this function using self.state
        # return y = h(x)
        phi =
        theta =
        psi =
        y = np.array([[phi], [theta], [psi]])
        return y

    def rk4_step(self, u: np.ndarray):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + P.Ts / 2 * F1, u)
        F3 = self.f(self.state + P.Ts / 2 * F2, u)
        F4 = self.f(self.state + P.Ts * F3, u)
        self.state = self.state + P.Ts / 6 * (F1 + 2*F2 + 2*F3 + F4)

    def M(self, state: np.ndarray, param_vals: list):
        # TODO Fill in this function
        #extract any necessary variables from the state and use them

        # Fill out M22, M23, and M33
        M22 =
        M23 =
        M33 =

        # Return the M matrix
        return np.array([[, , ],
                         [, , ],
                         [, , ]])

    def C(self, state: np.ndarray, param_vals: list):
        # TODO Fill in this function
        #extract any necessary variables from the state and use them

        # Return the C matrix
        return np.array([[],
                         [],
                         []])

    def dP_dq(self, state: np.ndarray, param_vals: list):
        # TODO Fill in this function
        #extact any necessary variables from the state

        # Return the partialP array
        return np.array([[],
                         [],
                         []])

    def tau(self, state: np.ndarray, u: np.ndarray, param_vals: list):
        """
        Returns the tau matrix as defined in the hummingbird manual.

        Parameters
        ----------
        state : numpy.ndarray
            The state of the hummingbird. Contains phi, theta, psi, and their derivatives.
        u : numpy.ndarray
            The input to the hummingbird. Contains f_l and f_r, the forces from the left
            and right propellers.
        param_vals : list
            A list of the physical parameters of the hummingbird that can be used in SymPy
            generated functions if needed.

        """
        # TODO Fill in this function
        # extract any necessary variables from the state

        # Return the tau matrix
        return np.array([[],
                         [],
                         []])


def saturate(u: np.ndarray, limit: float):
    for i in range(0, u.shape[0]):
        if abs(u[i,0]) > limit:
            u[i,0] = limit * np.sign(u[i,0])
    return u
