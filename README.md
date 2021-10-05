# InSAR_2D_decomposition_calculator
#psuedo 3-dimensional surface motion will be calculated from several InSAR velocity fields with one dimensional line of sight (LOS)
#view angles. We use psuedo 3-D motion because there are only two LOS directions with Sentinel-1; following multi-geometry data compilation (Fuhrmann and Garthwaite, 2019). By taking two Interferometric Synthetic 
#Aperature Radar Images (InSAR) from different satellite look directions (Ascending and Descending) decompose the LOS
#value from both angles to create a vertical and east-west motion map with the N/S motions mapped into vertical and EW- we call this psuedo-Vertical and Psuedo-EW. 

#All of these calculations depend on .grd files of a similar size and resolution of an AOI (area of intrest) 


#Step 1: grdcut you AOI from your dem.grd used to create the InSAR images:
grdcut topo/dem.grd -RW/E/S/N -Gdem_AOI.grd

#step 2: grdcut the same AOI from your los_ll.grd image. Do this for both asc and desc
grdcut los_ll.grd -Rdem_AOI.grd -GAscend_or_Descend_los_ll.grd

#step3:both LOS images need the same pixel size for this calculation to work, and they
#need to be reformatted. the grd increment needs to be changed so they are the same
#use grdinfo on both ascend and descend los_ll.grd files to find which has the largest
#x & y increments, and set the smaller increment file to the larger ones with grdsample:
grdsample Ascend_los_ll.grd -INEW_X/NEW_Y -Gnew_name.grd

#step 4: use grd2xyz to be able to import the data into the python calculator, again
#for both ascend and descending los AOI's
grd2xyz ascend.grd > ascend.xyz
grd2xyz descend.grd > descend.xyz

########Part 2: Calculate the incidence angles
#Step1: Convert the grdsample and grdcut los_ll.grd from part1:step3 to an XYZ for input
#into SAT_look
grd2xyz dem.grd > dem.xyz

#This step needs to be completed inside the topo/ directory for the master .PRM and .LED files

#Step 2: Use Sat_look to calculate the Up, East, and North to compute the look vectors
#Also ALOS_look and ENVI_Look for those sensors. output is:
#long lat elevation up east north
SAT_look master.PRM <dem.xyz> dem.lltn

#Pull out the pertinent data, which is only the look up vector
awk '{print $1, $2, $NF}' dem.lltn > incidence.lli

#Put this data into .grd format
gmt xyz2grd incidence.lli -Rdem_snip.grd -INEW_x/NEW_Y -fg -Glook_up.grd

#Use grdmath to calculate the incidence angles. arccos(look_up)= incidence angle
gmt grdmath look_up.grd ACOS = incidence_in_radians.grd

#Repeat these steps for both LOS datasets

########PART 3: import data into Python

#find the azimuth with SAT_baseline. Use the median Azimuth produced by this command
# put the azimuth directly into the python script; this is the same for every pixel

#run los_decomp.py
python los_decomp.px ascend.xyz incidence_ascend.xyz descend.xyz incidence_descend.xyz

########Part 4: finalize output

#change the output back into a .grd format for a finished product, for both
#East-West and Vertical components ready to import into your gmt mapping script:

xyz2grd output.xyz -Rdem_AOI.grd -INEW_X/NEW_Y -Goutput.grd

#EondOfLine
