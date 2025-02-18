import ReadNetworkData
import numpy as np
import sys
filename = 'TestSystem.txt'
bus_data,load_data,gen_data,line_data,tran_data,mva_base, bus_to_ind, ind_to_bus = ReadNetworkData.read_network_data_from_file(filename)

# print(f'Bus data: {bus_data}')
# print(f'Load data: {load_data}')
# print(f'Gen data: {gen_data}')
print(f'Line data: {line_data}')
# print(f'Transformer data: {tran_data}')
# print(f'MVA base: {mva_base}')
# print(f'Bus to index: {bus_to_ind}')
# print(f'Index to bus: {ind_to_bus}')
 

###

# Line Impedances => Line Admittances and susceptances
Za=1j*0.1+0.01;  Ya=1/Za;  b_a= 1j*0.0120/2
Zc=1j*0.2+0.03;  Yc=1/Zc;  b_c= 1j*0.0330/2
Zb=1j*0.25+0.02; Yb=1/Zb;  b_b= 1j*0.0210/2
N= 3#number of busses
# Bus addmitance Matrix
Ybus_=np.array([[Ya+Yc+b_a+b_c ,-Ya           ,-Yc           ],\
               [-Ya           , Ya+Yb+b_a+b_b,-Yb           ],\
                [-Yc           ,-Yb           ,  Yb+Yc+b_b+b_c]])

#print(f'Ybus_: {Ybus_}')

import LoadNetworkData as ld
Ybus , S_LD , buscode , ref , pq_index , pv_index , Yfrom , Yto , br_f , br_t , bus_labels = ld.LoadNetworkData(filename,)