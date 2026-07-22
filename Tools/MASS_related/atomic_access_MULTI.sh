#! /bin/bash

#N.B. - this needs updating for the new Azure MASS.

# Usage - need to log into the mass client. E.g., ssh -A -Y USERNAME@mass-cli.jasmin.ac.uk
# Then run this script directly.

#runs: suite IDs - can enter multiple suites.
#mass_dir: crum, devfc, etc.
#stream: set as apm.pp for monthly and apy.pp for annual means, aps.pp for seasonal.

#Examples:
#runs='u-dr061 u-dr226 u-dr240 u-dr241 u-dr292'; mass_dir='crum'; stream='apy.pp' #Annual means
#runs='u-dp448'; mass_dir='crum'; stream='apm.pp' #Monthly means
#runs='u-dp448'; mass_dir='crum'; stream='aps.pp' #Seasonal means
runs='u-dz438'; mass_dir='crum'; stream='apc.pp' #Bespoke usage file (e.g., UPC)

# -- Set the directory to save data to
savedir='PATH_TO_SAVE_DIRECTORY' #Don't use your home directory or it will get full!

#Set the time period for which to retrieve for

T1="{0001/01/01 00:00:00}"
T2="{9999/12/31 23:59:59}" #For all time periods.

#T1="{2005/12/01 00:01:00}" #
#T2="{2013/01/01 00:00:00}" #

echo Make sure you are logged into the mass client. E.g., ssh -A -Y USERNAME@mass-cli.jasmin.ac.uk
echo 'Retrieving for runs :-'

# Loop over the runs to retieve for
for run in $runs; do
	echo $i

	#A function for running the script
	run_script() {
	#        ~/scripts/atomic_access/atomic_access_generic_rose2 $run $mass_dir $stream $savedir $stash
		./atomic_access_func.sh $run $mass_dir $stream $savedir $stash "${T1}" "${T2}"
		#Quotation marks required if the variable string might contain spaces.
	}

#	stash='m01s00i004' # N.B., this type of specification doesn't work

        stash='34076' #Section 34, item 76 - NH3 on theta levels
        run_script

        stash='0408' #Section 0, item 408 - pressue on theta levels
        run_script

        stash='16004' #Section 16, item 4 - temperature on theta levels
        run_script

        stash='010' #qv (specific humidity) on theta levels - can calc RH this, pressure and temperature (or potemp)
        run_script

        stash='02' #U wind on theta levels
        run_script

        stash='03' #V wind on theta levels
        run_script

        stash='0150' #W wind on theta levels
        run_script

#        stash='5216' #Surface precip rate - this is in UPK
#        run_script


        #continue #use "continue" if you want to just get the above stash and ignore the ones below.




	echo 'Done atomic output for run ' $i

done #End of loop over runs
