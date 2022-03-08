#!/bin/bash

#splitter.sh uses split command to divide your files into pieces for the inversion. 
#Unless your survey area is very small, you will need to use the splitter then this 
#command to run the inversion 

for d in {00..89}
do
        python decomp_LOS.py los147_"$d" inc147_"$d" los09_"$d" inc09_"$d" "$d"
done

for d in {9000..9009}
do
        python decomp_LOS.py los147_"$d" inc147_"$d" los09_"$d" inc09_"$d" "$d"
done
