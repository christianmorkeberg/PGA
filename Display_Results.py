import numpy as np
def Display_Results(V,Ybus,Y_from,Y_to,br_f,br_t,buscode):
    """
    Display the power flow results in the Python command
    window. The function shall display both bus results and
    branch results. The bus results consist of displaying bus
    voltages and angles together with injected active and
    reactive power. The branch results consist of displaying
    the active and reactive power flowing into a bus.

    args: 
        V (np.array) - voltage vector
        Ybus (np.array) - admittance matrix
        Y_from (np.array) - admittance matrix for the from end of the branch
        Y_to (np.array) - admittance matrix for the to end of the branch
        br_f (np.array) - branch from indices
        br_t (np.array) - branch to indices
        buscode (np.array) - bus type code

    Apparent power flowing to the receiving ends of the branches is
    found by writing: S_to = V[br_t]*(Y_to.dot(V)).conj()
    The term Y_to.dot(V) gives the currents flowing from the
    branches into the receiving end busses
    V[br_t] ensures that the receiving end bus voltages become
    multiplied with the right receiving end current
    Similarly, the apparent power flowing into the sending end busses
    is: S_from = V[br_f]*(Y_from.dot(V)).conj()
    The injected power (generation and load) can be found by writing:
    S_inj = V*(Ybus.dot(V)).conj()
    When the power flows in the system have been calculated, they
    can be displayed in the iPython terminal window
    """

    # Calculate the apparent power flowing into the receiving end busses
    S_to = V[br_t]*(Y_to.dot(V)).conj()
    # Calculate the apparent power flowing into the sending end busses
    S_from = V[br_f]*(Y_from.dot(V)).conj()
    # Calculate the injected power
    S_inj = V*(Ybus.dot(V)).conj()

    # Display the results
    print('Bus results:')
    print('Bus  |  V  |  θ  |  P  |  Q')
    print('---------------------------------')
    for i in range(len(V)):
        print(f'{i+1}    | {np.abs(V[i]):.2f} | {np.angle(V[i],deg=True):.2f} | {np.real(S_inj[i]):.2f} | {np.imag(S_inj[i]):.2f}')

    print('\nBranch results:')
    print('From  |  To  |  P  |  Q')
    print('---------------------------------')
    for i in range(len(S_to)):
        print(f'{br_f[i]+1}    | {br_t[i]+1} | {np.real(S_to[i]):.2f} | {np.imag(S_to[i]):.2f}')

    print('\nBranch results:')
    print('From  |  To  |  P  |  Q')
    print('---------------------------------')
    for i in range(len(S_from)):
        print(f'{br_f[i]+1}    | {br_t[i]+1} | {np.real(S_from[i]):.2f} | {np.imag(S_from[i]):.2f}')
    
    return None