#!/bin/bash

#split each xyz file into sections so that python doesn't have memory error. This depends on the 
# survey area. My area, placed into ASCII format, had 416100 lines; I split this into 100 parts
# with -l 4161. change this for your own interferogram; use process.sh to run the inversion

split -l 4161 -d path147_true.xyz los147_
split -l 4161 -d path09_true.xyz los09_
split -l 4161 -d incidence_radians_147_cut.xyz inc147_
split -l 4161 -d incidence_radians_09_cut.xyz inc09_

#EOL
