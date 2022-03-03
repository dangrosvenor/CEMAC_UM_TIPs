#!/bin/bash -
#title          :get_era5_start.sh
#description    :
#instructions   :
#Source code    :
#Register       :
#author         :
#date           :
#updated        :
#version        :
#usage          :
#notes          :
#bash_version   : 4.2.46(2)-release
#============================================================================

# This script calls a python script that uses cdsapi to retrieve the required variables
# to run the UM from ERA5 data, it then creates a file named as per the Requirements for
# UM11.7 or suite:
#
# ec_grib_YYYYMMDDHHHH.t+HHH
#
# Older suites may need a differet name

year=2015
month=11
day=01
crun=3
run=24
spinup=24

echo "Retrieving global ${year}${month}${day} ERA5 data for ${run} hours in ${crun} intervals"

date=${year}${month}${day}
time_array=($(seq -s " " -f %02g 0 $crun $run))

for t in ${time_array[@]};
  do
  python get_era5.py ${date} --t ${t}
  cat surfacelevels.grib pressure.grib > ec_grib_${date}0${t}.t+0${t}
done

echo "Retrieving spin up of ${spinup} hours"
date2=`date -d "${date} - ${spinup} hours" +%Y%m%d`
time_array=($(seq -s " " -f %02g 0 $crun $spinup))
for t in ${time_array[@]};
  do
  python get_era5.py ${date} --t ${t}
  cat surfacelevels.grib pressure.grib > ec_grib_${date2}0${t}.t+0${t}
done
