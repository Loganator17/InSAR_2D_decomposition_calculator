#!/usr/bin/env python3
# Version 2.0
#Python 3.6.5

import numpy as np
import subprocess
import sys

asc_los = sys.argv[1]
asc_inc = sys.argv[2]
desc_los = sys.argv[3]
desc_inc = sys.argv[4]
name = sys.argv[5]

#clean up outputs prior to running calculator
cmd = 'rm outputs/output_up_'+name+'.xyz outputs/output_east'+name+'.xyz'
subprocess.call(cmd, shell=True)

A_data = np.loadtxt(asc_los)
D_data = np.loadtxt(desc_los)

#Define just the position data (long lat) from the imported data
pos_A = np.array(A_data[:,0:2])
pos_D = np.array(D_data[:,0:2])

#Define the los change for the calculator
los_A = np.array(A_data[:,2:3])
los_D = np.array(D_data[:,2:3])

#flight direction in radians- alpha values. This is different for every satellite path
Aalpha = -0.363115751
Dalpha = -2.7907815

#Synthesize omega, this shall be removed and import data will be used instead soon! 
A_inc = np.loadtxt(asc_inc)
D_inc = np.loadtxt(desc_inc)
aO = A_inc[:,2:3]
dO = D_inc[:,2:3]

#create the G matrix for the inversion 

G = np.zeros((2*len(A_data), 2*len(A_data)))

for i in range(0, len(A_data)):
        G[i*2,i*2] = -1*np.sin(aO[i])*np.cos(Aalpha)
        G[i*2,(i*2)+1] = np.cos(aO[i])
        G[(i*2)+1,i*2] = -1*np.sin(dO[(i)])*np.cos(Dalpha)
        G[(i*2)+1,(i*2)+1] = np.cos(dO[(i)])
X = np.linalg.pinv(G)@(v)

E=np.zeros(int(len(X)/2))
U=np.zeros(int(len(X)/2))

for i in range(0,len(E)):
        E[i] = X[i*2]
        U[i] = X[(i*2)+1]
E[E==0]=np.nan
U[U==0]=np.nan
a = E.reshape(len(pos_A),1)
b = U.reshape(len(pos_A),1)
x = np.concatenate((pos_A, a), axis=1)
y = np.concatenate((pos_A, b), axis=1)
np.savetxt('outputs/output_east_'+name+'.xyz', x, fmt='%.10f', newline=os.linesep)
np.savetxt('outputs/output_up_'+name+'.xyz', y, fmt='%.10f', newline=os.linesep)
print(name)

#EOL
