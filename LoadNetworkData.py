import numpy as np
import ReadNetworkData as rd
def LoadNetworkData(filename) :
    """
    This function loads network data from a file and generates the admittance matrix (Ybus), 
    branch admittance matrices (Yfrom, Yto), bus indices for branches (br_f, br_t), 
    bus codes, bus labels, and complex power loads at each bus (S_LD).

    args:  filename (str) - name of the file containing the network data
    
    returns:    Ybus (np.array) - admittance matrix
                S_LD (np.array) - complex power loads at each bus
                buscode (np.array) - bus codes
                ref (np.array) - reference bus index
                pq_index (np.array) - PQ bus indices
                pv_index (np.array) - PV bus indices
                Yfrom (np.array) - branch admittance matrix (from end)
                Yto (np.array) - branch admittance matrix (to end)
                br_f (np.array) - from bus indices for branches
                br_t (np.array) - to bus indices for branches
                bus_labels (np.array) - bus labels
    """
    def getAdmittance(R,X):
        """
        Calculate admittance from resistance and reactance 
        args:   R (float) - resistance in ohms 
                X (float) - reactance in ohms
        returns: (complex) - admittance in siemens
        """
        return (1/complex(R,X))

    ### I removed the global variables from the function because I don't like globals :) ### 
    ### Instead, I use return values ###

    #global Ybus , Sbus , V0 , buscode , ref , pq_index , pv_index , Y_fr , Y_to , br_f , br_t , br_v_ind , br_Y ,S_LD , \
    #ind_to_bus , bus_to_ind , MVA_base , bus_labels , br_MVA , Gen_MVA , \
    #br_id , br_Ymat , bus_kv , p_gen_max , q_gen_min , q_gen_max , v_min , v_max

    #read in the data from the file...
    bus_data , load_data , gen_data , line_data , tran_data , mva_base , bus_to_ind , ind_to_bus = \
    rd.read_network_data_from_file(filename)

    MVA_base = mva_base
    N = len(bus_data) #Number of buses
    M_lines = len(line_data)
    M_trans = len(tran_data)
    M_branches = M_lines + M_trans
    Ybus = np . zeros ( ( N , N) ,dtype=complex)



    # Generate Ybus
    for fr in range((N)): # For each from
        for to in range((N)): # For each to
            if fr == to: # Diagonal
                for line in line_data:
                    if line[0]-1 == fr or line[1]-1 == fr: # Line[0] = from bus, Line[1] = to bus, Note that the bus numbers are 1-indexed
                        Ybus[fr,to] += getAdmittance(line[3],line[4]) + complex(0,line[5]/2) # Line[3] = R, Line[4] = X
            else: #Non diagonal
                for line in line_data:
                    if line[0]-1 in [fr,to] and line[1]-1 in [fr,to]:
                        Ybus[fr,to] = - getAdmittance(line[3],line[4]) # Line[3] = R, Line[4] = X
    
    #print(f'Ybus = \n {Ybus}\n')
    # Generate Yfrom 
    Yfrom = np.zeros((M_branches,N),dtype=complex)
    for br in range((M_branches)): # For each line (branch?)
        from_bus = line_data[br][0]-1 #zero index
        to_bus = line_data[br][1]-1 #zero index
        Yfrom[br,from_bus] = getAdmittance(line_data[br][3],line_data[br][4])+complex(0,line_data[br][5]/2)
        Yfrom[br,to_bus] = -getAdmittance(line_data[br][3],line_data[br][4])
    #print(f'Yfrom = \n {Yfrom}\n')

    # Generate Yto 
    Yto = np.zeros((M_branches,N),dtype=complex)
    for br in range((M_branches)): # For each line (branch?)
        from_bus = line_data[br][0]-1 #zero index
        to_bus = line_data[br][1]-1 #zero index
        Yto[br,from_bus] = -getAdmittance(line_data[br][3],line_data[br][4])
        Yto[br,to_bus] = getAdmittance(line_data[br][3],line_data[br][4])+complex(0,line_data[br][5]/2)
    #print(f'Yto = \n {Yto}\n')

    # Generate Bus indices for the branch from and to ends: br_f, br_t
    br_f = np.zeros((M_branches),dtype=int)
    br_t = np.zeros((M_branches),dtype=int)
    for br in range((M_branches)): # For each line (branch?)
        br_f[br] = line_data[br][0]-1 #zero index
        br_t[br] = line_data[br][1]-1 #zero index

    # Generate Buscode
    buscode = np.zeros((N),dtype=int)
    for bus in range((N)):
        buscode[bus] = bus_data[bus][4] #bus_type (integer value) ## <- failing here

    pq_index=np.where(buscode== 1)[0]# Find indices for all PQ-busses
    pv_index=np.where(buscode== 2)[0]# Find indices for all PV-busses
    ref=np.where(buscode== 3)[0]# Find indices for the reference bus

    # Generate bus_labels
    bus_labels = np.zeros((N),dtype=str)
    for bus in range((N)):
        bus_labels[bus] = bus_data[bus][1] #e.g. BUS1HV 

    # Generate Array with the complex power load at each bus: S_LD
    S_LD = np.zeros((N),dtype=complex)
    if len(S_LD) != len(load_data[0]):
        raise Exception('Length of S_LD and load_data do not match')
    for load in load_data:
        S_LD[load[0]-1] = complex(load[1],load[2])

    # Generate Sbus (complex power injection at each bus, i.e. both load and generation)
    Sbus = S_LD.copy()
    for gen in gen_data:
        Sbus[gen[0]-1] = complex(gen[1],gen[2])


LoadNetworkData('TestSystem.txt')


# exec(open("LoadNetworkData.py").read())
# exec(open("test.py").read()) 