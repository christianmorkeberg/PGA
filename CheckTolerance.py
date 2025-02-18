import numpy as np
def check_Tolerance(F,n,err_tol):
    '''CheckTolerance(F,n,err_tol) \n
        Checks whether the greatest mismatch in the mismatch
        vector is smaller than the specified tolerance. Could also
        be used to display the absolute value of the greatest
        mismatch as well as the iteration number.

        returns:
            success (bool)

        args: 
            F (np.array) - mismatch vector
            n (int) - iteration number
            err_tol (float) - tolerance
    '''

    #Hint: normF = np.linalg.norm(F,np.inf), returns thegreatest absolute value of the column vector F
    normF = np.linalg.norm(F,np.inf)
    if normF < err_tol:
        success = True
    else:
        success = False

    return success
