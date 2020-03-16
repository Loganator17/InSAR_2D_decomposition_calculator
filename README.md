# InSAR_2D_decomposition_calculator
#3 dimensional surface motion will be calculated from several InSAR velocity fields with one dimensional line of sight (LOS)
#view angles. In order to find a model of dike propagation and closing, it is possible to calculate the three dimensional 
#surface motion from multi-geometry data compilation (Fuhrmann and Garthwaite, 2019). By taking two Interferometric Synthetic 
#Aperature Radar Images (InSAR) from different satellite look directions (Ascending and Descending) decompose the LOS
#value from both angles to create a vertical and east-west motion map. 


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


########Part 2: Calculate the incidence angles
#Step1: Convert the grdsample and grdcut los_ll.grd from part1:step3 to an XYZ for input
#into SAT_look
grd2xyz Ascend_or_Descend_los_ll.grd > Ascend_or_Descend_los_ll.xyz

#This step needs to be completed inside the intf_all/InSAR# for .PRM and .LED files

#Step 2: Use Sat_look to calculate the Up, East, and North to compute the look vectors
#Also ALOS_look and ENVI_Look for those sensors. output is:
#long lat elevation up east north
SAT_look S1_20170917_ALL_F1.PRM < Ascend_or_Descend_los_ll.xyz > asc_incidence_data.xyz


#Step 2: incidence = arctan(look_U/sqrt(look_E^2+look_N^2)) output is in degrees, need
#to convert to radians for the correct incidence angle


########PART 3: import data into Python

#find the azimuth with SAT_baseline. Use the median Azimuth produced by this command
# put the azimuth directly into the python script


########Part 4: finalize output

#change the output back into a .grd format for a finished product, for both
#East-West and Vertical components ready to import into your gmt mapping script:
xyz2grd output.xyz -Rdem_AOI.grd -INEW_X/NEW_Y -Goutput.grd
