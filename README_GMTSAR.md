# InSAR_2D_decomposition_calculator
#psuedo 2-dimensional surface motion will be calculated from one ascending and one descending InSAR velocity fields with opposing one-dimensional line of sight (LOS) view angles (Fuhrmann and Garthwaite, 2019). By taking two Interferometric Synthetic Aperature Radar Images (InSAR) from different satellite look directions (Ascending and Descending) decompose the LOS value from both velocity fields to create a vertical and east-west motion map with the N/S motions mapped into vertical and EW- we call this psuedo-Vertical and Psuedo-EW. 

#All of these calculations depend on .grd files of a similar size and resolution of an AOI (area of intrest) 

#Step 1: grdcut an AOI from the dem.grd used to create the InSAR images:
grdcut topo/dem.grd -RW/E/S/N -Gdem_AOI.grd

#step 2: grdcut the same AOI from your los_ll.grd image. Do this for both asc and desc
grdcut los_ll.grd -Rdem_AOI.grd -GAscend_or_Descend_los_ll.grd

#step3: Using grdinfo on both ascend and descend los_ll.grd files to find which has the largest 
#x & y increments, and set the smaller increment file to the larger ones with grdsample:
grdsample Ascend_los_ll.grd -INEW_X/NEW_Y -Gnew_name.grd

#step 4: use grd2xyz to be able to import the data into the python calculator, again
#for both ascend and descending los AOI's
grd2xyz ascend.grd > ascend.xyz
grd2xyz descend.grd > descend.xyz

########Part 2: Calculate the incidence angles
#Step1: Convert the grdsample and grdcut los_ll.grd from part1:step3 to an XYZ for input
#into SAT_look. Complete this task in the topo/ directory
grd2xyz dem.grd > dem.xyz

#Step 2: Use Sat_look to calculate the Up, East, and North to compute the look vectors
#Also ALOS_look and ENVI_Look for those sensors. output is:
#long lat elevation up east north
SAT_look master.PRM <dem.xyz> dem.lltn

#Pull out the pertinent data, which is only the look up vector
awk '{print $1, $2, $NF}' dem.lltn > incidence.lli

#Put this data into .grd format
gmt xyz2grd incidence.lli -Rdem_snip.grd -INEW_x/NEW_Y -fg -Glook_up.grd

#Use grdmath to calculate the incidence angles. arccos(look_up_radians)= incidence angle
gmt grdmath look_up.grd ACOS = incidence_in_radians.grd

#Repeat these steps; both LOS datasets need corresponding incidence angle information

########PART 3: import data into Python

#find the azimuth with SAT_baseline. Use the median Azimuth produced by this command
# put the azimuth directly into the python script; this is the same for every pixel

#run decomp_LOS.py
#for larger datasets, use splitter.sh and process.sh to complete each decomposition in sections
#This is necessary, as larger datasets will max out the python memory limit for the inversion.

python los_decomp.px ascend.xyz incidence_ascend.xyz descend.xyz incidence_descend.xyz

########Part 4: finalize output

#change the output back into a .grd format for a finished product, for both
#East-West and Vertical components ready to import into your gmt mapping script:

xyz2grd output.xyz -Rdem_AOI.grd -INEW_X/NEW_Y -Goutput.grd

#EOF
