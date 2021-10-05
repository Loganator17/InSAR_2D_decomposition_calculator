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

#clean up outputs prior to running calculator
cmd = 'rm output.xyz output_east.xyz output_up.xyz'
subprocess.call(cmd, shell=True)

A_data = np.loadtxt(asc_los)
D_data = np.loadtxt(desc_los)

#Define just the position data (long lat) from the imported data
pos_A = np.array(A_data[:,0:2])
pos_D = np.array(D_data[:,0:2])

#Define the los change for the calculator
los_A = np.array(A_data[:,2:3])
los_D = np.array(D_data[:,2:3])

#flight direction in radians
Aalpha = -0.363115751
Dalpha = -2.7907815

#Synthesize omega, this shall be removed and import data will be used instead soon! 
A_inc = np.loadtxt(asc_inc)
D_inc = np.loadtxt(desc_inc)
aO = A_inc[:,2:3]
dO = D_inc[:,2:3]

#create the 4 elements for the matrix used for the inversion 

o11=-1*np.sin(aO)*np.cos(Aalpha)
o12= np.cos(aO)
o21=-1*np.sin(dO)*np.cos(Dalpha)
o22= np.cos(dO)


#run the inversion row by row
n=0
for n in range(0,416100):
     A = np.array([[o11[n,:], o12[n,:]], [o21[n,:], o22[n,:]]])
     d = np.array([los_A[n,:], los_D[n,:]])
     X=np.linalg.pinv(A).dot(d).T
     with open('output.xyz', 'a') as outfile:
          for slice_2d in X:
               np.savetxt(outfile, slice_2d)
     n = n+1

     if n==416101:
          break

#Load in the output file 
output = np.loadtxt("output.xyz")

x = np.concatenate((pos_A, output[:,0:1]), axis=1)
y = np.concatenate((pos_A, output[:,1:2]), axis=1)
np.savetxt('output_east.xyz', x, fmt='%.7f')
np.savetxt('output_up.xyz', y, fmt='%.7f')

#This produces the min and max, which is useful for the scale bars in GMT script
print('east')
print('-T', np.amin(output[:,0:1]),"/",np.amax(output[:,0:1]))
print('vert')
print('-T', np.amin(output[:,1:2]),"/",np.amax(output[:,1:2]))

#EndOfLine
