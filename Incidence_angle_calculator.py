#!/usr/bin/env python3
# Version 1.0
#Python 3.6.5

import numpy as np
import subprocess
import sys

inFile = sys.argv[1]
outFile = sys.argv[2]

#Incidence angle calculation: incidence = arctan(look_U/sqrt(look_E^2+look_N^2)) 
#output is in degrees, need 
#to convert to radians for the correct incidence angle


I_data = np.loadtxt(inFile)
I_d = np.nan_to_num(I_data, copy=False)
up = I_d[:,5:6]
north = I_d[:,4:5]
east = I_d[:,3:4]

omega_deg = np.arctan(np.divide(up,(np.sqrt((east**2)+(north**2)))))
omega = np.radians(omega_deg)

with open(outFile, 'a') as o:
     for i_a in omega:
          np.savetxt(o, i_a)


#EOF
