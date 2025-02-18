import numpy as np
def generate_Derivatives(V,Ybus):
    """
    Calculates the values of the derivatives of the apparent power
    with respect with voltage magnitude dS/dVm, and the derivative of
    the apparent power in respect to the voltage angles dS/dθ .These
    values are later used to construct the Jacobian matrix.

    returns:
        J_dS_dVm (np.array) - dS/dVm
        J_dS_dTheta (np.array) - dS/dθ
    
    args:
        V (np.array) - voltage vector
        Ybus (np.array) - admittance matrix
    """

    # Initialize the Jacobian matrices
    J_ds_dVm=np.diag(V/np.absolute(V)).dot(np.diag((Ybus.dot(V)).conj()))+ \
             np.diag(V).dot(Ybus.dot(np.diag(V/np.absolute(V))).conj())

    J_dS_dTheta = 1j*np.diag(V).dot((np.diag(Ybus.dot(V))-Ybus.dot(np.diag(V))).conj())

    return J_ds_dVm,J_dS_dTheta