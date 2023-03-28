UM common issues


[TOC:Contents:6]



Emailing for help




• If there is a problem (that is not on this list) then it is worth emailing Monsoon.

monsoon@metoffice.gov.uk
Also, CMS might be useful. Note new procedure :-

Dear All,

On Thurs 1st July 2021 the NCAS-CMS Modelling Helpdesk will move to a new Discourse Forum available at https://cms-helpdesk.ncas.ac.uk (Note new URL).

The current helpdesk will then become read-only.  Any active queries will be moved to the new system.

To raise a new query (topic) you will need to sign up for an account at the above URL. 

Please read the following “Welcome” post for further information: 

https://cms-helpdesk.ncas.ac.uk/t/welcome-to-the-ncas-cms-modelling-support-forum/7







UM known failure points Met Office website
Has some useful information on known failure points for general UM issues :-
https://code.metoffice.gov.uk/trac/um/wiki/KnownUMFailurePoints
Getting start dumps
If you have access to MASS you can try, e.g. (adapt for the file you want) :-
moo get moose:/opfc/atm/global/rerun/201403.file/2014031500_glm_t+0 .
You can search the directories using :-
moo ls
There is some more information here too :-
http://cms.ncas.ac.uk/wiki/UM/MesoscaleModelling
The Code Repository


Code.metoffice.gov.uk
Should have a password  for this (email  via Paul, etc.).
Replaces the code on PUMA - do all of this on the rose server.
Need to cache the password. 
Do this first :-
https://code.metoffice.gov.uk/trac/home/wiki/FAQ
Then this :-
https://code.metoffice.gov.uk/trac/home/wiki/AuthenticationCaching


Copying a Rose suite




• Can copy using command line :-

○ rosie copy u-aj097

○ Faster than invoking the "rosie go" GUI, although this is another option :-

• rosie go --prefix=u     - the prefix=u part is very important.

○ Can search for users in the search space at the top right.

§ e.g. adrianhill for Adrian.

○ To copy a job - right click and copy.







Shutting down a Rose suite


rose suite-shutdown --name="suitename" 

• if you can't shut it down, log onto excyl cylc server and kill jobs (ssh exvmscylc)

○ (Will give the process names when you try and restart using rose suite-run --restart. Kill -9 these

• Or, 

○ ps -fu ${USER}

§ N.B. - make sure that the X-window is wide enough, or it will not show the run ID to identify the different suites.

 


kill



 

This is the PID for the PPID=1 python process for your suite.

Then remove the port file:

 

rm $HOME/.cylc/ports/

 

That will kill the suite.



Unable to connect to suites, won't shut down, unresponsive, stalled suite


Update:16:20: Still not sure what's caused this, and a number of people are affected, but the advice (thanks Matt Shin) is as follows:

1) login to exvmscylc and kill the lead process of the running suite (the one that's a parent of all the others)

ps -fu ${USER}

2) If no processes remain, also delete your ~/cylc-run/SUITE/.service/contact files as well. (Normally, these files are removed automatically by cylc, but they may be lingering due to an abnormal shut down.)

Hopefully this will sort things out... AJ.



I've had a few reports of this nature today.

[plvida@exvmsrose:~/roses/u-am164]$ cylc stop u-al508

Cannot connect: https://exvmscylc.monsoon-metoffice.co.uk:43004/command/set_…:

[plvida@exvmsrose:~/roses/u-am164]$

This is a new one on me; I'm raising with other experts for help. More news when I have it.



• This happened to me - the solution was to delete the file in contact/ (no. (2) above).





Clean a Rose suite


rose suite-clean --name=mi-ae162 : clear up suite - start from fresh - removes execs and ancils



Output


• Namelists and pe_output goes to :-

○ /projects/asci/dgrosv/cylc-run/u-ab157/work/20081112T0000Z

○ Shortcut script . ~/cdpe 

• Pp files go to (for e.g.)

○ /projects/asci/dgrosv/cylc-run/u-ab157/share/cycle/20081112T0000Z/VOCALS/1p0_L70/ukv/um

○ Shortcut script . ~/cdpp - need to modify for non-VOCALS runs.

• Rose .out and .err files for the various stages :-

○ ~/cylc-run/u-ab157/log/job/20081112T0000Z

○ (these are the ones that can be accessed by right clicking on a job in the rose sgc tree).

• Ancil files (e.g.) :-

○ /projects/asci/dgrosv/cylc-run/u-ab218/share/data/ancils/Iceland/4p0_L70/

○ e.g. xconv qrparm.orog  (from postproc)





Stash



• Um option on lefthand side of "rose edit "suite

○ Um_ / namelist / Model Input and Output / Stash Requests 

○ Also have Time Profiles and Usage Profiles here

• Can search for variables too (Filter box).

• After adding domains (time, domain, usage) need to run these macros to 

• Macros

○ Top two with red dots - tidystashtransform and tidy*prune

• Roses//app/um

○ rose-app.conf

§ Gives info on the stash at the end.

§ Although this does not give the variable name, and so perhaps not that useful.

§ File 

□ app/um/file/STASHmaster/STASHmaster_A

® Contains a list of all the diags and their numbers I think

® Can grep for ones required - might not all have been output, though.

® E.g. to search for cloud amounts/fraction :



◊ grep -i amount ~/roses/u-ab793/app/um/file/STASHmaster/STASHmaster_A





® Also, the info here gives you the stash number - the 2nd and 3rd entries h numbers of the first row give the section number and the item number. So in this case :-

® The item would be section 0, item 2, or code 0-002



○ Exporting the stash for importing into another job

○ Rose macro stash_copy.STASHExport

§ Have to enter the filename in double quotes.







Adding new stash items using the namelist


• Can add them manually using the namelist :-

○ app/um/rose-app.conf

○ When adding new items need to give them a unique stash code number in the line :-

§ [namelist:streq(1)]

○ I.e., the "1" here. 

○ They don't have to be proper stash indices (e.g., "d17228fb"), can just do 1, 2, 3, etc.

○ Then run rose edit and run the stash transform macro and it will convert them into proper stash indices.





Adding new usage etc. profiles


• Did this via the text file (e.g. see  u-ai864/app/um/rose-app.conf)

○ Need to add text in two places :-



[namelist:nlstcall_pp(pp1)]

file_id='pp1'

!!filename='unset'

filename_base='$DATAM/${RUNID}a_pb%N'

l_reinit=.true.

packing=1

reinit_end=-1

reinit_start=0

reinit_step=6

reinit_unit=1

reserved_headers=0



And



[namelist:use(d50be24f)]

file_id='pp1'

locn=3

!!macrotag=0

use_name='ice_vars_3d'



○ The key points are that have changed pp0 to pp1, changed the filename_base to use *a_pb* instead of *a_pa* and have given it a different use_name. The other stuff was the same.

○ Might need to re-run the macros for the stash items after adding these.

○ Can also do this by cloning the profile in rose edit.

§ Probably cloning is the best approach - had some trouble with the above approach - may due to the way I named the profiles?







Copying stash from one job to another



• Can do it just be editing the file 

○ app/um/rose-app.conf

§ Search for "streq" and can just copy and paste the required stash values.

§ Need to do this for the time, domain and file profiles.

§ Then can just re-open rose edit - might need to run that macro too.





• Other method - Sounds like the method below is not working properly yet…

○ Instructions from Paul :-

Hello

I seem to have had some luck with the stash export/import. I’m not 100% sure about what its doing but this transplanted stashfrom one suite to another....

 

in app directory of donor suite (e.g. app/um)

rose macro stash_copy.STASHExport

 

keep pressing return until finished (about 12 times!). Most files the same . I’ve seen that one is different, but i don’t know why.

 

Cd into app directory of target suite

rose macro stash_copy.STASHImport

Value for stash_donor_job (default None): "/home/h01/frfp/roses//app/um/STASHexport.ini"

 

Keep repeating file path entry until  the macro stops (again about 12 times in my case)

○ But Phil says :-

I’ve just been trying this and I can’t get it to work. I get the following output after I put the pathe in for the ini file

 

[prosen@exvmsrose:~/roses/u-ac194/app/um]$ rose macro stash_copy.STASHImport

Value for stash_donor_job (default None): /home/prosen/roses/u-ac174/app/um/STASHexport.ini

Traceback (most recent call last):

  File "/usr/lib64/python2.6/runpy.py", line 122, in _run_module_as_main

    "__main__", fname, loader, pkg_name)

  File "/usr/lib64/python2.6/runpy.py", line 34, in _run_code

    exec code in run_globals

  File "/home/fcm/rose-2016.02.0/lib/python/rose/macro.py", line 1286, in

    main()

  File "/home/fcm/rose-2016.02.0/lib/python/rose/macro.py", line 1281, in main

    opts.validate_all, verbosity

  File "/home/fcm/rose-2016.02.0/lib/python/rose/macro.py", line 934, in run_macros

    reporter=reporter)

  File "/home/fcm/rose-2016.02.0/lib/python/rose/macro.py", line 1074, in _run_transform_macros

    macro_name=transformer_macro

  File "/home/fcm/rose-2016.02.0/lib/python/rose/macro.py", line 1096, in apply_macro_to_config_map

    return_value = macro_function(macro_config, meta_config)

  File "/home/fcm/rose-2016.02.0/lib/python/rose/macro.py", line 1071, in

    opt_non_interactive))

  File "/home/fcm/rose-2016.02.0/lib/python/rose/macro.py", line 732, in transform_config

    res = get_user_values(optionals)

  File "/home/fcm/rose-2016.02.0/lib/python/rose/macro.py", line 1143, in get_user_values

    options[k] = ast.literal_eval(user_input)

  File "/usr/lib64/python2.6/ast.py", line 49, in literal_eval

    node_or_string = parse(node_or_string, mode='eval')

  File "/usr/lib64/python2.6/ast.py", line 37, in parse

    return compile(expr, filename, mode, PyCF_ONLY_AST)

  File "", line 1

    /home/prosen/roses/u-ac174/app/um/STASHexport.ini

    ^

SyntaxError: invalid syntax

 

 

I’ve tried moving the file and using relative paths, but always something similar.

 

I’m about to post on the Leeds UM list to see if anyone else has had any success

 

Phil







Changing wallclock time of global model


○ Look in suite-runtime-dm.rc in your roses directory. Search for walltime. This will control the driving model. Paul's is set at 15 minutes.

○ Also, can do trigger --> edit in rose sgc and change the submission script - not sure what it will do with the subsequent runs, though (have changed in script above, but this did not affect the failed run - will prob have to stop the suite and restart).

§ Actually, this doesn't seem to work…. It didn't change the wall clock time.

§ Although it did say 15 mins from qstat.. Maybe it was working??



○ N.B. - the above does not work for v10.8.

§ Looks like it is set in :-

□ rose-suite.conf:DM_WALL_CLOCK=500

§ But can also change in rose edit in General run options.



Changing wallclock for forecast job

§ rose-suite.conf

§ Change WALL_CLOCK_LIMIT  



Changing for reconfiguration job

○ Search for walltime in the following files. Is located in several sections - change the one with "UM reconfiguration" heading above  :-

§ For global model :-

□ suite-runtime-dm.rc

§ For LAM :-

□ suite-runtime-lams.rc







Changing the project for a rose suite


• Add :-

○ "-P = "

• to the submisson options in suite-runtime-dm.rc and suite-runtime-lams.rc (if want to change for both global and LAM).

○ I.e. just below where walltime is set (change everywhere that this is set in those two files).



• Also, for datadir :-

$DATADIR is typically set in .profile, but can be set differently for individual jobs/suites as required. To do so, add the following at the top of the rose-suite.conf file :-



root-dir{share}=*=/projects//$USER 

root-dir{work}=*=/projects//$USER



This will tell the suite to direct all output to /projects//$USER.



Pasted from <https://collab.metoffice.gov.uk/twiki/bin/view/Support/NEXCS> 









Misc


• Hasnan function - can test any array, vector, etc. for occurrence of NaN - slows the code down though.





Compiling with Rose


• Presumably won't need to stop and re-start the suite after editing the code? Can hopefully just re-trigger the compile process from rose sgc.

• This seems to work.

• Although might have to trigger fcm_make_lam as well as fcm_make2_lam

○ Had to do this when had a wrong module specified.

○ Probably best to do this every time - doesn’t take long for the first stage.

• N.B. - can point to local copy in rose-app.conf by specifying the path to the directory instead of the branch name - e.g. /projects/asci/dgrosv/um_code/vn10.3_coupling2/

○ Think need the / at the end, but not 100%. Works with it on anyway.

• Had one compiler error where it could not make a module, but didn't say much more than that - turns out there was a variable specified in there that had been specified in another module. Once it was taken out it was ok.





Holding all the jobs in Rose


• rose suite-run -- --hold

○ Sets all the jobs to HOLD.

○ Then can run individual ones.



Rotated pole
The nested suites can use a rotated pole whereby the model grid is treated as though the centre of the domain is on the equator. This means that the regularly-spaced grid in latitude and longitude that the nested suites use is closer to a regularly-spaced grid in real distance than it would be if the nest was nearer the poles (due to the lines of longitude getting closer together in terms of distance at higher latitudes).

Here is an example Python function to unrotate the pole and get the actual lat/lon coordinates for a nested domain with rotated pole. See the next entry for where to find the pole latitude and longitude :-



def read_lat_lon_UM(cube,pole_lat,pole_lon):



        import iris.analysis.cartography as iac  #required for unrotate pole, etc.



        iglobal=0

        try:

                lat_read = cube.coord('grid_latitude').points

                lon_read = cube.coord('grid_longitude').points

        except:

                lat_read = cube.coord('latitude').points

                lon_read = cube.coord('longitude').points

                iglobal = 1





        nX = len(lon_read)

        nY = len(lat_read)





        #Get the shape of the arrays (i.e. number of elements in array in each dimension

        #These arrays are single vectors of size e.g. 500 x 1 

        sh_lat = lat_read.shape

        sh_lon = lon_read.shape





        #replicate the 1D arrays in 2D arrays using the shapes of the other array (e.g. shape of lat for the lon replication)

        lat2d=np.tile(lat_read,[sh_lon[0],1])

        lon2d=np.tile(lon_read,[sh_lat[0],1])



        lon2d_2=lon2d

        lat2d_2=np.transpose(lat2d)  #Transpose (swap dimensions) of the 2D lat array to make it correspond to the location on a 2D grid



        if iglobal==0:

                #Unrotate the pole using the IRIS utility

                lon, lat = iac.unrotate_pole(lon2d_2, lat2d_2, pole_lon, pole_lat)

        else:

                lat = lat2d_2

                lon = lon2d_2





        return (lat,lon,sh_lat,sh_lon,nX,nY,iglobal)





Pole lat and lon


• Can be found in e.g. :-

○ /home/d02/dgrosv/cylc-run/u-ab218/log.20160201T153530Z/job/20140831T0000Z/Iceland_4p0_L70_ukv_um_fcst_008/NN/job 

(As POLE_LAT and POLE_LON).





Using different revisions of the trunk


• Trying using this in the rose-app.conf file :-

○ casim_sources=https://code.metoffice.gov.uk/svn/monc/casim@409

§ Didn't work…

• This worked, though :-

○ casim_sources=svn://puma.nerc.ac.uk/monc.xm_svn/casim/trunk@409



18.25-3.90 = 14.35 



Comparing different suites on monsoon (differences between suites)


Use the online tool, e.g. :-  https://code.metoffice.gov.uk/trac/roses-u/browser/a/f/5/0/1/

• Just click on view changes and then can compare two different suites at any revision required.

• Can also send a link to someone else using this method to show them the diffs.









Revision changes (online) for Rose suites


• E.g. :-

○ https://code.metoffice.gov.uk/trac/roses-u/browser/a/d/8/0/9

○ Just replace with the name of the rose suite required.

○ Then can go to revision log and view changes etc.





Where to find the suite revision that was actually run


• In e.g.  directory ~/cylc-run/u-ad809/log  :-

rose-conf/20160705T094053-restart.version:Revision: 15208

rose-conf/20160705T094053-restart.version:Last Changed Rev: 15208

rose-conf/20160705T094053-restart.version:--- rose-suite.conf   (revision 15208)

rose-suite-run.version:Revision: 15208

rose-suite-run.version:Last Changed Rev: 15208

rose-suite-run.version:--- rose-suite.conf      (revision 15208)







Changing timestep


• Namelist method (or can do in rose edit) :-

○ roses/rose-suite.conf:rg01_rs01_m01_dt=15

○ Is an option in rose edit  for no. timesteps in period :-

§ UM - namelist - top level - model domain and timestep

§ , but does not work on its own (do both have to be changed?)



• N.B. - is also possible to separately change the mphys timestep (via mphys_switches.F90 using max_step_length - not tried this, though).







Runtime errors involving BicGstab


       These are hard to diagnose but I have once or twice found they can be caused by problems or instabilities introduced by settings in the radiation scheme. 

See also https://code.metoffice.gov.uk/trac/um/wiki/KnownUMFailurePoints. Mohit suggests that in global runs it may help to change n_conv_calls from 2 to 3 

in the convection scheme for a few days. Other possibilities include just changing the model timestep or the microphysics substep. 



Bounds checking



Hi Dan

 

I have not tested this, so you may need to do some trial and error but the way to turn on bounds checking is as follows.

1)      In the top-level branch  of the coupling code directory cd to fcm-make/meto-xc40-cce

a.       The flags used for normal compile can be found in um-atmos-high.cfg

2)      Add a line with the syntax

build-atmos.prop{fc.flags}[um/src/] = $fcflags_common –R b

The –R b does the bounds check I think. As with previous version of the UM I would not apply bounds checking to the whole UM as it will fail where you may not expect it to fail

 

Hope this is a help

 

Cheers

 

Adrian



Also from Adrian :-

• It depends what you want to bounds check – do you just want to check CASIM or is there stuff in jonathans branch that you want to test?

○ If it is the latter, I would suggest that you need to create a branch from Jonathans and then edit the config in your new branch and build that.

• In your rose_app.conf (under your suite) I think you need to change your config_revision and config_root_path to your revision and your branch and then any changes you make in your branch will be picked up (I think)

• I do not think the line below will work because micro_main does not exist un um/src/

○ Trying um/src/atmosphere/large_scale_precipitation/CASIM/micro_main.F90

○ Actually should be casim/micro_main.F90 I think. The /projects/vaci/dgrosv/cylc-run/u-af368/share/fcm_make_lam/extract/um folder contains the coupling side of CASIM :-

aerosol_casim_couple_switches.F90  casim_prognostics.F90                 lbc_cloud_ice_number.F90

aerosol_extract_return.F90         casim_set_dependent_switches_mod.F90  mphys_casim_diagnostics.F90

casim_check_in_fields.F90          casim_switches.F90                    mphys_casim_um.F90

casim_check_out_fields.F90         casim_work_arrays.F90                 read_aerosol_profile.F90

casim_ctl.F90                      check_casim_diags.F90                 scm_code_tmp.F90

casim_driver_name.F90              cld_frac_scheme.F90                   ship_tracks.F90

casim_drivers_list.F90             diaghelp_um.F90                       stub

○ Whereas micro_main.F90 etc. are inprojects/vaci/dgrosv/cylc-run/u-af368/share/fcm_make_lam/extract/casim/ :-



○ Since this is the general path usually followed to micro_main.F90. E.g. see :-

§ /projects/vaci/dgrosv/cylc-run/u-af250/share/fcm_make_lam/extract/um/src/atmosphere/large_scale_precipitation/CASIM/micro_main.F90

○ So will try :-

§ build-atmos.prop{fc.flags}[casim/micro_main.F90] = $fcflags_common -R b







• Notes :-

○ N.B. - do this in the UM side of the code (not rose suite).

○ Also, need to set the conf branch to use this (and e.g. not Johnathan's).

○ Have also just noticed that there is a folder called :-

§ monsoon-xc40-cce  (as opposed to meto-xc40-cce).

§ It seems to have the same files in it - maybe this one should be used for Monsoon and not the other one?

○ Paul suggests modifying the extract directory on Monsoon once it has done the install (and then compiling) to make sure the file has been changed.













Making it use the BCs (boundary conditions) from previous global runs on disk (not same suite).


• Rose edit --> Driving model --> 

○ For RUN_MODE set to Use files on disk

• Then add the path to the cb files created previous LAM folders, e.g. ;

○ /projects/asci/dgrosv/cylc-run/u-ab218/share/cycle/20140831T0000Z/glm/um/umglaa_cb???

§ Remembering the ??? Wildcard

○ Not sure how this would work when using cycling?

§ Maybe change the date to be YYYMMDD ?

§ Trying :

□ /projects/asci/dgrosv/cylc-run/u-ad809/share/cycle/2014mmddT0000Z/glm/um/umglaa_cb???



• Could use this technique - although might have to copy the cb files, etc. to the correct dir structure :

○ Re-starting just the forecast job (with cylcling)







Issue with there being more than 60 files in namelist (failure of *frame* jobs) for making boundary conditions.


• Change to the correct suite name in this python script :-

○ /home/d02/dgrosv/scripts/hack-frame-namelists_DPG.py

• Also set N to be the number of hours in each CRUN.

• Run the python script (from any directory).

• Then change the bash script :-

○ run_hack-frame-namelists.sh

• To add in the suite name and the frame number to start from.

• Then set the *frame* jobs to suceeded in rose sgc (to cause the createbc jobs to start).







Rosebush online viewer



• From rose server :-

○ firefox http://localhost/rose-bush/suites?user=$USER 2>/dev/null &

○ This will open a page with the list of your active suites and you can use the 'job lists' tab to check status of the tasks.



716381544/1e6=716.3815      4294967296/1e6 = 4294.9673 



Pasted from <http://collab.metoffice.gov.uk/twiki/bin/viewfile/Static/SystemMonitoring/Reports/latest_quota_report.txt>











 

Checking disk quota



• This one is actually more readable:-

○ https://collab.metoffice.gov.uk/twiki/bin/viewfile/Static/SystemMonitoring/Reports/quota_summary.txt

• More detailed, but not as clear version :-

• https://collab.metoffice.gov.uk/twiki/bin/viewfile/Static/SystemMonitoring/Reports/lustre_multi

• Think is only updated daily.

• Can also do :-

○ quota.py -g nexcs-n02 lustre_multi



• The numbers here appear different to the above, so maybe this is more real-time?

• This is where I found the info:-

○ https://collab.metoffice.gov.uk/twiki/bin/view/Support/FileSystems#Quotas

• *** Had a problem in Jan 2018 where I could not write large files to /projects/ (error saying "No space left on device" even though the projects were  not over-quota. It seems that there is an individual limit, but that other people's files were contributing (not sure which files since I was at 40TB, but asci alone was using 67TB.)

○ Anyway can diagnose with this command :-

quota.py -u lustre_multi



Disk quotas for user dgrosv (uid 30308):

Filesystem           TB    Quota       %  |      Files      Quota       %

--------------  -------  -------  ------  |  ---------  ---------  ------

/.lustre_multi    43.38    60.00   72.29  |    6995635          0    0.00

§ 

○ (My quota was raised to 60 TB - and then to 80 TB).









Supercomputer quota
You can type "aboutme" on Monsoon and then look at the "Fairshare" value. This goes from -12 (bad) to +12 (good). If you have low values then your runs will be penalised relative to the other supercomputer jobs (so you will have to wait longer before they run). The Fairshare value depends on whether and by how much you have gone over your quota.





Issue of Rose not showing the run length for the nests.


• Need to set FREE_RUN to FALSE to get this back (I guess it is a bit of a bug since if not using cycling then the free_run switch should be irrelevant).





Re-starting a run using the start dumps from part way through (with cylcling)


Hi Dan,



I think you can fix your suite, but it is a bit of a pain and one of those things where it would be much easier for me to help you if you were here.



The first thing to do is take a temporary copy of your entire suite data directory. Then at least you can revert back to it if something goes horribly wrong!



I would do the following:



1.       Shutdown the suite (if it is still running), open up the rose edit GUI and change the INITIAL_CYCLE_POINT to 20140906T0000Z.  File --> Check & Save.

2.       Retrieve the archived startdump for 20140906T0000Z and place it here: /home/dgrosv/cylc-run/u-af178/share/cycle/20140906T0000Z/Iceland/4p0_L70/ukv/ics/ukv_astart

3.       Type rose suite-run -- --hold to relaunch your suite in a held state. You should now see the tasks for 20140906T0000Z in the graph.

4.       Right-click on each task from 20140906T0000Z that you do not need to re-run (definitely glm_um_recon and Iceland_4p0_L70_ukv_recon) and select Reset state -> succeeded. Do the same any start-up tasks (fcm_make, ancils, etc). If you still have the LBCs for the regional model for the 20140906T0000Z cycle then you can do the same for all the Iceland_4p0_L70_ukv_um_frame/createbc tasks (I hope so otherwise things will be more complicated!)).

5.       Select Control -> Release suite to unpause the suite. It should then just run on to do the global and regional model forecast tasks for the 20140906T0000Z cycle, then continue as normal for the 20140907T0000Z cycle and on to completion. I hope.



Cheers,



Chris





• Tried this for u-af178 and it seemed to work ok.





Re-starting just the forecast job (with cycling)


• Want to re-run just the forecast job, but the previous days bubble in rose sgc in not accessible.

• Trying to follow the procedure as above for u-ai864

• Will do rose-suite run -- --hold

○ This should start the suite again, but will pause allowing me to set the glm tasks to succeeded.

○ Note, probably not worth worrying about setting the frame and makebc tasks for the forecast jobs to succeeded, since is not much computation to do these I think.

○ So, just right click each glm top header and set to succeeded.

§ Note, the next day will only appear once have done this for the day before since only shows one day at a time.

○ Set all of these to suceeded :-

§ Install x2; ancil, build x2

○ But also have to keep HOUSEKEEPING for the starting day to waiting since otherwise it starts the next fcast job following link previous (using the dump created before presumably)

§ This will now not run until the fcast of the 1st day is finished.

○ The Control-release suite - seems to have worked - at least the fcast job is submitted.





Issues with app/fcm_make/rose-app.conf file and compilation


• For a new run (u-ag688)  I was getting errors at the fcm_make_lam and fcm_make_glm stages :-



[FAIL] fcm make -f /work/projects/vaci/dgrosv/cylc-run/u-ag698/work/20081112T0000Z/fcm_make_lam/fcm-make.cfg -C /home/dgrosv/cylc-run/u-ag698/shar

e/fcm_make_lam -j 4 mirror.target=xcm:cylc-run/u-ag698/share/fcm_make_lam mirror.prop{config-file.name}=2 # return-code=255

Received signal ERR

cylc (scheduler - 2016-10-03T11:23:33Z): CRITICAL Task job script received signal ERR at 2016-10-03T11:23:33Z

cylc (scheduler - 2016-10-03T11:23:33Z): CRITICAL failed at 2016-10-03T11:23:33Z

[FAIL] /work/projects/vaci/dgrosv/cylc-run/u-ag698/work/20081112T0000Z/fcm_make_lam/fcm-make.cfg:6: reference to undefined variable

[FAIL] extract.location{diff}[casim] = 

[FAIL] undef($casim_sources)



• The rose-app.conf file looked like this at the start :-

meta=um-fcm-make/vn10.3



[env]

casim_rev=vn0.0

casim_sources=/projects/asci/dgrosv/um_code/r1098_r328_casim_cloud_scheme969

!!casim_sources=fcm:casim.xm_br/dev/danielgrosvenor/r1098_r328_casim_cloud_scheme969@1683

!!casim_sources=fcm:casim.xm_br/dev/danielgrosvenor/r328_casim_cloud_scheme@1592





  • Seemed that just by swapping the commented out casim_sources lines with the uncommented one (i.e. so that commented ones appeared first) then it worked ok…???



• Annette says that there is a GUI for fcm_make - using this might be safer and with fewer headaches because of these issues.





OMP threads (factor of 2 increase in no Pes over what is expected)




* If OMP_NUM_THREADS is set to more than 1 (e.g. N) in suite-runtime-lams.rc then the number of nodes used will be N times bigger than would be expected from from just the number of processors in x and y as set in the GUI.

* This is setting the number of Open MP tasks.

* In older UM versions Open MP did not produce much speedup (e.g., a 10% increase for a OMP_NUM_THREADS=2 for v8.5, or possibly v10.3, can't remember).

* But asking for N times as many nodes might produce much larger queuing times.

* In newer versions it is possible that the Open MP speedup is more efficient, but likely it is better to use more normal nodes first?



* Can also get some speedup by setting :-

○ {% set HYPERTHREADS = 2 %}

○ This uses the same no. PES,  but runs two threads per PE. Think gives around a 10% speedup.











Checking to see the code that was actually compiled


• Look in e.g. :-

○ ~/cylc-run/u-aq608/share/fcm_make_lam/extract/

○ Has folders for casim and um where can find the respective code files that were compiled.



Switching off tracer BL mixing


• Done in the rose suite :-

○ app/um/rose-app.conf:l_bl_tracer_mix=.false.



Start files in .pax format


They are packed. I’m downloading them to 

/projects/asci/frfp/startfiles/*QU00.20090301.pax



There are 5or 6 of them. You need to unpack them to find which one has the start file in it using this command.



pax -rf coprr.??QU00.20090301.pax

cd op/daily/datawgl

and then its something like: qwqu00.T+0 



cheers

Paul





Postprocessing on xcs


Can run e.g. xconv by doing :-

$UMDIR/bin/xconv

Can run Python, but have to do this first :-

                module load scitools



Script from Mohit for converting from 360 to Gregorian :-


® Copied from Hamish's :-

◊ ~hamgo/scripts_namelists/mod_dates.sub

® Copied the script and amended it to work for me :-

◊ /home/d02/dgrosv/py/ukca/cal_360_to_Greg/mod_dates.sub

◊ Points to the ancils in $UMDIR.

◊ Run from the dir where you want to write them - amended files will be put in out/ folder.



Set MASS storage from double copy (duplex) to single copy (simplex)




® Hello Everyone

We’ve been asked to ensure that our archiving is single-copy rather than duplex on the mass archive. You can’t change the old ones, but for new ones you can fix the issue by changing the mkset command in the ‘install_cold/opt’ app in the options file: rose-app-monsoon-cray-xc40.conf

to include the –single-copy (otherwise default is duplex).

 

[command]

default=moo mkset --single-copy -p project-${CHARGING_CODE} moose:/devfc/$ROSE_SUITE_NAME || true



N.B. - I can only find these files that fit the bill, so presumably it must be them :-



$ grep -ri "moo mkset" *

 

app/install_cold/opt/rose-app-monsoon.conf:default=moo mkset -p project-$PROJECT moose:/devfc/$ROSE_SUITE_NAME || true

app/install_cold/opt/rose-app-mo.conf:default=moo mkset moose:/devfc/$ROSE_SUITE_NAME || true





Preventing deletion of *da* dumps


Could be this line in :-

® suite-runtime-dm.rc:

® suite-runtime-lams.rc

ls -tr *a_da* | head -n -1 | xargs --no-run-if-empty rm

® Testing in job u-ax336







Using gui aerosol profile input instead of namelist file


® Since in v10.8 the namelist file option is read in many times causing slowdown and file issues.

® Instructions from Jonathan :-

Meanwhile, if you wish to move to using the GUI:

1)    Open the GUI and change casim_aerosol_couple_choice to be ‘Free Tracers (gui).

2)    Save and close the GUI.

3)    Use the attached python script to convert your namelist into a text file. Hopefully the instructions within should be helpful.

4)    Replace the namelist: run_casim_tracer in your UM rose-app.conf file with the values you get from the text file.

5)    Reopen the GUI and check that the tracer input all looks sensible.

6)    Check and Save and submit a short test job – hopefully you should get the same answers as your previous runs.

7)    If you need to change your aerosols again, do so in the GUI.

 

Eventually, my intention is to remove the namelist (external file) option altogether, but I’m keeping it there for a while to let people transfer over.

® Conversion script is saved in :-

◊ C:\Users\Dan\Documents\logbook\Leeds_2013\research\UM\scripts\namelist_to_gui.py

® And on Monsoon :-







Python IRIS WGDOS unpack error


® ???

® Is an error that occasionally occurs when trying to access data from a cube using IRIS.

® Seems to not happen if have an embed point before the command and then continue (so that it is running in ipython I guess).

® So, one option could be to run the script from ipython.

◊ Type "ipython" to load it.

◊ Then run DRIVER*.py

◊ Seems to work ok.

® The other could be to copy the files to JASMIN and run from there as the error doesn't seem to occur there.



Disk full messages due to log files


® Not sure if this is the cause, but this is where they are:-

◊ /home/d02/dgrosv/cylc-run/suite_name/log/

® Perhaps more likely to be the quota on this :-

◊ quota.py -u lustre_multi

◊ See here : Checking disk quota





Number of land points nlandpts recon error


® Number of land points error in recon for nest

○ Looks like with Hamish's new suites, the number of land points is written to a text file here :-

§ ~/cylc-run/*job_name*/share/data/ancils/Iceland/4p0_L70/nlandpts

○ Check in job.out what it should be set to. Error (see job.out) looks like :-



                        No of land points in output land_sea mask     =  90000

                        No of land points specified in namelist RECON =  64012

                        Please correct the number of land points, via the gui, updating LAND_FIELD within SIZES



                        ????????????????????????????????????????????????????????????????????????????????

                        ???!!!???!!!???!!!???!!!???!!!       ERROR        ???!!!???!!!???!!!???!!!???!!!

                        ?  Error code: 50

                        ?  Error from routine: Setup_LSM_Out

                        ?  Error message: Number of land points does not agree with input namelist!

                        ?  Error from processor: 0

                        ?  Error number: 3834

                        ????????????????????????????????????????????????????????????????????????????????









○ In this case set it to 90000



Nudging global model in VN11.7 nesting suite
As well as switching on nudging and pointing it to the directory with the ERA5 nudging files in I had to :-

Add a stash request for 30-451, TALLTS and a nudging macro.
 N.B. - tried adding this directly to app/glm_um/opt/rose-app-ukca.conf, but it didn't seem to get picked up. Had to add in the rose edit GUI. Might be ok with the codes indicated in the changeset below (30451_b3dae44a, etc.).
Also, needed to make sure that used enough PEs - was failing with 8x10 processors with a seg fault.
Mohit identified this as a lack of memory :-
"The job.err showed errors from malloc which is the basic memory allocation function, plus the traceback pointed to a random line in UKCA, which was not modified (only Nudging turned On)."
So, once set back to 16x18 again it worked (could experiment with fewer to use fewer nodes to get through queues quicker if a problem - but would need to reduce CRUN length).
See this changeset for what was done (ignore the changes related to emissions) :-

https://code.metoffice.gov.uk/trac/roses-u/changeset?reponame=&new=196867%40c%2Ff%2F1%2F4%2F5&old=196667%40c%2Ff%2F1%2F4%2F5


"No hosts selected" upon rose suite-run
Had an error saying that no host was selected.
Had to change the xc40 host to :-
HOST_XC40='xcs-c'
In rose-suite.conf_monsoon and rose-suite.conf
Still didn't submit.
Then had to change this in rose-suite.conf :-
ACCOUNT_USR='asci'
Jobs now submit.
