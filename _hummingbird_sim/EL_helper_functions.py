import sympy as sp 

def calc_omega(R): 
    """
    omega = calc_omega(R)
    Description:
    Calculates the angular velocity vector from a rotation matrix

    Parameters:
    R - 3x3 sympy matrix representing a rotation matrix, must be parameterized
    by dynamicsymbol variables that are functions of time. 

    Returns:
    omega - 3x1 sympy matrix representing the angular velocity vector
    """
    t = sp.symbols('t') 
    R_dot = R.diff(t)  #lab manual does R_dot = R.diff(q)@q.diff(t) 
    #R_dot2 = sp.Matrix(sp.zeros(3,3))
    #for i in range(len(q)):
    #    R_dot2 = R_dot2 + R.diff(q[i])*q[i].diff(t)
    #R_dot = R_dot2
    skew_matrix = R_dot@R.T
    omega = sp.Matrix([skew_matrix[2,1], skew_matrix[0,2], skew_matrix[1,0]])
    return sp.simplify(omega.reshape(3,1))

def find_coeffs(vector, q_dot):
    """
    coeffs = find_coeffs(vector, q_dot)

    Description:
    Finds the coefficients of a sympy vector with respect to a vector of 
    dynamicsymbols that are functions of time. The result will be a matrix of
    coefficients that when multiplied by the q_dot vector will give the original
    vector. 

    Parameters:
    vector - a 3x1 sympy matrix representing either linear velocity or angular velocity
    q_dot - a sympy matrix representing the time deriviative of the generalized coordinates

    Returns:
    coeffs - a matrix that is (3 x len(q_dot)) that contains coefficients such that 
             coeffs@q_dot = vector
    
    """
    coeffs = sp.zeros(3, len(q_dot))
    for i in range(len(vector)):
        for j in range(len(q_dot)): 
            collected = sp.collect(sp.expand(vector[i]), q_dot[j])
            coeffs[i,j] = collected.coeff(q_dot[j])
    return sp.simplify(coeffs)


def rotx(theta):
    """
    R = rotx(theta)
    Description:
    Returns a 3x3 matrix representing a rotation about the x axis

    Parameters:
    theta - float or sympy symbol represention rotation about the x axis, we assume
    that theta is in radians

    Returns:
    R - a 3x3 sympy matrix representing the rotation about the x axis
    """

    R = sp.Matrix([[1, 0, 0],[0, sp.cos(theta), -sp.sin(theta)], [0, sp.sin(theta), sp.cos(theta)]])
    return R

def roty(theta):
    """
    R = rotx(theta)
    Description:
    Returns a 3x3 matrix representing a rotation about the y axis

    Parameters:
    theta - float or sympy symbol represention rotation about the y axis, we assume 
    that theta is in radians
    
    Returns:
    R - a 3x3 sympy matrix representing the rotation about the y axis
    """
    R = sp.Matrix([[sp.cos(theta), 0, sp.sin(theta)], [0, 1, 0], [-sp.sin(theta), 0, sp.cos(theta)]])
    return R

def rotz(theta):
    """
    R = rotx(theta, radians=False)
    Description:
    Returns a 3x3 matrix representing a rotation about the z axis

    Parameters:
    theta - float or sympy symbol represention rotation about the z axis, we assume
    that theta is in radians

    Returns:
    R - a 3x3 sympy matrix representing the rotation about the z axis
    """

    R = sp.Matrix([[sp.cos(theta), -sp.sin(theta), 0], [sp.sin(theta), sp.cos(theta), 0], [0, 0, 1]])
    return R