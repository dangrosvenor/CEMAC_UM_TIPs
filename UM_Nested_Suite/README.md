# UM-Rose starter guide

This is based on the document originally produced by Phil Rosenberg, so thanks to him. Some information may be out of date, though - let us know if you find that something doesn't work and we can update it.

For some alternative instructions on some of these things and more trouble-shooting advice, also see this page :- [[UM_common_issues]]

[TOC:Contents:6]

## Monsoon

Monsoon is the Met Office supercomputer accessible by their collaborators. This document describes getting the UM to run on Monsoon using the Rose interface.

You will need 3 accounts to use Monsoon. The first is a Monsoon account (obviously). The second is a Met Office Science Repository Service (MOSRS) account which allows you access to the UM source code. The third is a Collab Twiki account, which will give you access to the (slightly scattered) documentation.

### Logging in 


You will need a Monsoon account to start with. This needs to be organised with your Met Office Collaborator so speak to them. Once you have this you can log in via "Lander" and from there can log onto the xcs machine. From here you can copy, edit and run rose suites/jobs.

&ensp; `ssh –Y username@lander.monsoon-metoffice.co.uk`

&ensp;  `ssh -Y xcsc`


### Set Up


In order to be able to grab the source code from the repository you will need a Met Office Science Repository Service (MOSRS) account. This will have a username that is different to your Monsoon account and a regular password. You need to make sure that FCM (see below) knows this user name and the password is cached. To do this follow the instructions at https://code.metoffice.gov.uk/trac/home/wiki/FAQ under the configuring subversion access and then at https://code.metoffice.gov.uk/trac/home/wiki/AuthenticationCaching.


## Rose

Rose is the interface for setting up a um run. You create a suite for each run you want to do and tell rose things like what source code you want to use to build the UM, the science settings, the variables you want to output etc. When complete you can submit the suite for running and will be show progress by a Cylc flow diagram. 

### Creating a new job

In your home directory you will find a folder called roses, which holds all your rose jobs. Each has a subdirectory, e.g. u-ab138. The u stands for universal and basically all jobs will have this u prefix.

Probably the best thing to do is to copy an existing suite that was set up to do similar things to what you want to do. You can do this from the command line using :-

`rosie copy <suite-name-to-copy>`

The copy will come from the fcm repository (so make sure your source job has had its changes committed) and your new job will have a space in the repository (more later). There is also the rosie create command - I've not tried this. See rosie create --help for more info.

Or you can use the following command for a GUI :-

`rosie go --prefix=u`

Which will open the rose GUI and you can search for a job to copy. Select this job and hit the copy button. 

## Editing Rose jobs
You can edit the suites by cd'ing into the roses/<suite-ID> directory and then typing:-
 `rose edit`
 
 This opens the editing GUI. You will probably make most of your changes, but it may also be necessary to edit the underlying namelist/text files for some things.



### Setting up which project account to use

Each project has an allocated number of hours, and your priority on the Monsoon queue decreases as you use them up. If you don’t set up a project then I’m not sure what happens - it seems to mean you queue for ages in my experience.

This is set (in rose edit) under 👎
 `suite conf -> Nesting Suite -> General run options as "CHARGING_CODE"

Insert the name of your project account. You should then be able to make use of your allowance.



### Editing and running a job

All the following commands should be run from the job’s directory, i.e. ~/roses/<job_id>/


#### Editing a job


If you have just created a job then the Rose GUI will already be displayed. If not then to edit a job run

`rose edit&`



This will pop up the following rose window



When you have finished editing click the Abc icon to check your changes and save or just hit the save icon to save without checking. Note that if you save changes without checks and then do a save and check the checking will only be performed on new changes. However it looks like the ? icon will check everything for you.

If you are interested then each of the options on the left hand side of the edit window corresponds to a directory in ~/roses/<job_id>/app, and within this folder is a file called rose-app.conf which contains all the data for the options in that section. When you click a greyed out option rose basically parses the options in the appropriate .conf file to display. The exception is the suite conf section which has its rose-app.conf file in the ~/roses/<job_id>/ directory. In fact if you run rose edit from inside one of the app directories it brings up an edit program for that directory only. You can if you wish manually edit these files. But if you do so then it would be a good idea to then run rose edit and hit the ? button to force check the things you have modified - you may need to open the appropriate app down the left hand side before you do the checks.

Note some options are greyed out. If you click on them then the editor will load the module for that section. When you validate your job only loaded modules are checked.



#### Re-using existing executables

Note that if you wish to reuse an already built executable from another suite, the executables get built in the directory

`~/cylc-run/<job_id>/share/fcm_make_lam/build-atmos/bin/um-atmos.exe`



When selecting the number of processors to use, you may wish to bear in mind that each node contains two sockets, each with 16 processors (32 processors per node). I think Monsoon has 128(ish) nodes. If a socket has to access memory the other socket on the same node this is slower than accessing its own memory, but faster than on another node.



#### Wallclock Time

If you wish to change the wallclock limit for your nested domains you do so under 

`suite conf->jinja2:suite.rc->General`

run options. This sets the wallclock limit for all domains I think. However It does not change the global forecast wallclock limit. To change the global walclock limit you must edit the file 

`~/roses/<suite_id>/suite-runtime-dm.rc`


and change the value of the appropriate -l walltime entry. Note there are two such entries, one for the reconfiguration and one for the forecast. You can find which is which by scrolling up from the entry and checking the comments.



#### STASH and Setting Output

You can set all your output under UM->namelist Model Input and Output. To add new streams go to Model Output Streams, right click and add new. You can then edit it. The same applies to Domain Profiles, Time Profiles and Usage Profiles which are under Stash Requests and Profiles. The idea is that you set up files (under model output streams), with an associated usage profile (under usage profiles), time intervals/meaning (under time profiles) and spatial regions (under domain profiles). When you add a variable you then select the usage, time and domain profile for each variable.

You should note that one file can have a maximum of 4096 levels worth of data and it can contain data from multiple C runs. The 4096 levels can be any combination of multiple levels from 3d variables, single level variables and from a range of consecutive time steps. Note that you can change how often you start a new file under the model output stream with the variable reinit_stap

To set a variable to output, go to STASH Requests and Profiles->STASH Requests. Hit the New button (top right) to open the add new STASH request dialog and select the variables you want. When you close that button you need to select the domain, time and usage profile for each variable. 

When specifying rho or theta levels the possible range is from 1-n_levels inclusive. N_levels will generally be 70 but you can check under suite conf->jinja2:suite.rc Nested Region n setup->Resolution n setup. The option you need to check is rg01_rs01_levset; L70 indicates 70 levels.

If you want to export your stash then go to ~/roses/<job_id>/app/um and run 

`rose macro stash_copy.STASHExport`

If you want a different name then enter it but in must be in quotes. The macro will ask you the name over and over again. If you keep putting the name in and hitting enter then eventually it will stop, however we are fairly sure that after the first time you can hit ctrl+x to kill it. To import a stash list to another job put the export file in the same loation in the new suite and run 

`rose macro stash_copy.STASHImport`


IMPORTANT: The STASH variables and profiles are identified by hashes, but when you first create then they are given indices starting from one. These indices must be replaced by the hashes. Also the hashes are a function of the variable contents so if you modify any of these things you need to update the hash. The reason for doing this is that duplicated items can be quickly identified and removed if needed. To update all your hashes go to Stash Requests and Profiles->STASH Requests and click Macros (top left). Then select stashindices.TidyStashTransform. You can also see a macro here to prune duplicates ad another to check the validity of your STASH variables.


#### Source Code/build

You can edit these things under the fcm_make option or if you are interested you can find the controlling file under ~/roses/<job_id>/app/fcm_make/rose-app.conf


#### Committing your changes to the repository

This enables you to allow others to copy your latest rose suite and keeps a history of your suite so if you ever break things you can go back.

`fcm status`

`fcm diff`

`fcm commit`


These show which files have changed, how the files are different and commits your changes to the repository creating a point you can always restore back to. It is good practice to do this whenever you make a change and only change one (group of) thing(s) at once between commits so you can easily find where something broke. It is bad practice to just commit at the end of the day, or end of the week, or when you remember.



#### Building the executables, reconfiguring and running the model

There are three steps to running the UM, first build the reconfiguration and simulation executable, then running the reconfiguration, which creates the input files you need for the run, then running the simulation. Note that once you have built the executables and run the reconfiguration, if you wish to run the simulation again then you don’t need to do these two steps - unless you have done a rose suite-clean or rose run --reset which clears out all these files. Note if you are nesting, then there is an additional step of creating ancillary files for the nesting domains and running the global model. Again if you have done these already you can turn them off for subsequent runs.



To switch on/off what gets built as part of the executable building go to fcm_make->env->Make steps. Here you can also decide whether you wish to extract the source again or use the source that you have already downloaded. Then you can decide which high level things get built, i.e. the global model and each nest.  To do this go to suite conf->jinja2:suite.rc->Driving model setup and suite conf->jinja2:suite.rc->Nested Region N setup, resolution N setup->Config N setup. I think that if the build new executable is ticked under jinja2:suit.rc then the options from fcm_make are applied for that config and you will see a fcm_make_* branch in the Cylc flow chart, otherwise nothing is built for that config.



To switch on/of building nested ancillaries and switch on/off rerunning the global simulation go to suite conf->jinja2:suite.rc->Driving model setup



To run the model after exiting the rose edit program type the following command

`rose suite-run`

This will run the job from the beginning and will pop up the Cylc flow diagram which shows the job progress. The following other commands are useful.

Some other useful variations are

`rose suite-run --restart`

`rose suite-run --new`

`rose suite-scan`

`rose suite-gcontrol`

`rose sgc`

`rose suite-clean`

`rose suite-shutdown`

`qstat_snapshot –u <user_id>`


The restart option restarts a run that had stopped from the point that it stopped. To do this first hit the stop/halt button in the Cylc gui otherwise you will see an error message about the suite still running (you can reopen the gui using rose sgc - see below). The new option deletes the cylc-run/<suite_id>/ directory before it runs the job. This includes things such as all output files, all ancilliaries, all log files for all cases when this suite has been run. Rose sgc is shorthand for rose suite-gcontrol and pops up the cylc flow diagram for a job that is currently running. Note that if the job has crashed or finished when you do this you may get an error saying cannot open port and the view will just have the suite number in the middle and perhaps an error message bottom left. To get the view up you need to do rose suite-run --restart. Rose suite-scan is similar to -llq as is qstat_snapshot; use qstat_snapshot –h for help. Note qstat_snapshot must be run on the supercomputer 



Rose suite-shutdown will kill a run that has for example crashed. However if you still have some parts of the job running or queuing then you must instead open the cylc viewer right click and kill to stop them, otherwise rose suite-shutdown will silently fail.



## Output


On completion you should find all your data in 

`~/cylc_run/<run_id>/share/cycle/<date_time>/<domain_name>/<res_name>/<exp_name>/um/`


where all the items in angle brackets are things you set in the rose editor. Although if you do auto archiving this data should be removed and it will all be on Mass - see below.



You can also find the stderr and stdout for each of the bubbles in the cylc diagram in the ~/cylc_run directory. If the suite is still running then these files will be in ~/cylc_run/<suite_id>/log. The files for the most recent run of a suite will be in ~/cyc_run/<suite_id>/log/job ( the log directory is a link to log.yyyymmddThhmmssZ in the same directory). Previous runs are archived in tar.gz log files with the date and time appended. In ~/cylc_run/<suite_id>.

There is also a lot of log type info under ~/cyc_run/<suite_id>/work/YYYYMMDDTHHMMSSZ/<run_name>_<crun_number>. The log files contain output from node 0 of your run, if you want to find output from all your nodes you can find it the pe_output subdirectory of the abouve directory. In that directory you can also find core dumpsand STASHmaster files.



## Running “Operationally”


If you wish to do repeated runs whenever a new Met Office global forecast is produced, for example to do forecasting for a field campaign then these instructions indicate how.

In rose you need to go to suite conf->jinja2:suite.rc->Driving model setup and select RUN_MODE to be Follow operational suite. Then go to suite conf->jinja2:suite.rc->Cycling options and set INITIAL_CYCLE_POINT, FINAL_CYCLE_POINT and CYCLE_INT_HR to be the start time of your first forecast, the start time of your last forecast and the time period between forecast starts. I think CRUN_LEN needs to be 3 hours (1 hour failed for me, but 3 hours worked - I think that might be because the global model uses 3 hours) and your lbc frequency for your nested region(s) should probably be 10800.

You now need to arrange for someone at the MO to put the global files somewhere where you can access them. This could be anywhere in the /project/ directory as I think everyone gets read access to these. Then open the file ~/roses/<suite_id>/bin/install_startdata and find the line beginning opdir = and opanalysis = in the get_oper_filenames function. Replace the directory and filename with the location of your global files.

Now when you run the suite it should attempt to run each forecast and wait until the appropriate global data arrives in the file as expected before running.

Note that when you save and check in the Rose GUI, it appears that the check grabs the current time and if there has been another global run between your INITIAL_CYCLE_POINT and the current time then it complains. It seems that it is okay to ignore this error providing your file naming convention for global data include the date/time for identification.



## Dealing with errors


You can find some information if you have a crash by right clicking on the bubble in Cylc and going to view job stderr. You can see these error messages in the .err files in the log directory. These files may indicate that a core dump was made - which includes all the memory at the time of the crash. You can find the core dumps in the ~/cylc_run/<suite_id>/work/… directory for the crun in question as described above in the output section. They will have filenames like core.atp.<some_number>.<node_number> To look at the core dump you need a debugger and to know which binary created the dump. The binary will usually be at something like ~/cylc-run/<suite_id> /share/fcm_make_lam/build-atmos/bin/um-atmos.exe, but you can check by doing 

`file <core_dump_file_name>`

You can examine the core dump with Allinea Forge DDT debugger. You must do this from the xcm computer and you will need X window forwarding using the -Y option

`ssh -Y xcm`

`module load forge`

`ddt`


Ensure you select allinea DDT on the left then select Open Core. Select the executable and add core dump and hit OK. You will see the stack and can browse through the source to see where the crash happened.

You can do interactive debugging too. In your rose directory find where ROSE_LAUNCHER is set. This will probably be in a file called suite-runtime-*.rc, you can search for the right file by doing grep -rnw . -a “ROSE_LAUNCHER”. Change the value from aprun to module load forge; ddt-mpirun. Now do the following

`ssh -Y xcm`

`module load forge`

`ddt`


Go to File->Options and select job submission. For the template file select  Click Run. Make sure the application is your UM applicationThen go to options->job submission 



### Further Info


You can find a quick reference guide for rose at http://metomi.github.io/rose/doc/rose-quick-ref.html

There is also documentation on the MO Twiki http://collab.metoffice.gov.uk/twiki/bin/view/Support/ROSENestingSuite



## Moose/MASS


MASS is the tape archive. It is good to put things there because it saves you space. You can automatically archive your data from rose using the *_arch options for your nest under 

`suite conf->jinja2:suite.rc->Nested Suite region n setup->Resolution n setup->Config n setup.`

If you look under archive->arch then you will see the location of the archive.

IMPORTANT note that in order to do the auto archiving you must first create the set using moo mkset as detailed below.

There is a command line interface for Mass called Moose, there is a user guide at http://collab.metoffice.gov.uk/twiki/bin/viewfile/Static/MASS/user_guide.html. On Monsoon you can only use moose from the xcm computer not xvmsrose. On Jasmin you can only use it from the mass-cli1 machine and you need to follow the setup at http://collab.metoffice.gov.uk/twiki/bin/view/Support/ExMASSUserSetUpGuide.

The mass archive is set up in a particular fixed hierarchy directory structure specific files must be placed in specific directories. In fact there is no way to create or delete directories (except for sets - see below). When you send a file to mass if the directory it needs to go in is not there then it will be created and if you delete all the files in a directory then the directory will automatically be deleted. The file paths known as moose URIs always begin with

`moose:/<data_class>`

 where data_class represents the broad category of the data and must be one of: adhoc( no naming conventions - can be used for anything), crum (climate runs), devfc (development forecasts), ens (ensembles?), misc (?), opfc (operational forecasts?). I have access to devfc, so I will use that to describe how things work. Note that other data classes can have different hierarchies/structures so consult the docs.

In devfc the URI will look something like (note that the / immediately after the : is optional)

`moose:/devfc/<data_set>/field.file/<filename>`
`field.pp/<filename>`
`lbc.file/<filename>`


As you might expect, fields files must go in the field.file folder and pp files must go in the field.pp folder, boundary condition files must go in lbc.file. I think that netcdf files can be uploaded too, but not sure of the folder.

Before you can upload anything you need to create a set for it to go in. In devfc the set must be the UMUI job id (all 5 characters) or the Rose suite id. The syntax is 


`moo mkset -v --project=project-<projectName> moose:/devfc/<jobId>`

Here -v means verbose, so isn’t strictly necessary.

You can view the contents of a moose: directory using

`moo ls <moose_url>`

Where the url can be as short as blank which implies just moose: or as far down the structure as needed.



To pull data out of mass you create a query which specifies things like the times, variables, averaging times etc of the data you want then use a moo select command which specifies the query and the data you wish to check. The query is placed in a file and it is the filename used on the command lne. For example, we could put the following query in a file called lowCloudQuery



<pre>

begin

item = 203

section = 9

end

</pre>



Note that the low cloud variable is in section 9 item 203 in STASH. Then use the following moo command

<pre>

moo select -C lowCloudQuery moose:/devfc/u-ac174/field.pp/ lowCloud.pp

</pre>

This will pull out all the data that matches the query in the lowCloudQuery file (which is all low cloud data) from the moose:/devfc/<rose_suite>/field.pp/ collection and it will put them in the lowCloud.pp file on the local machine. The -C option causes all the data to be included in a single output file, otherwise the data will be put in the same number of files as contain data in the archive.

Items within a begin end block are ANDed together - i.e. in the example we want data with item code 203 and section code 9. If we put multiple begin end blocks in a file then these are ORed together to make the query. So if we wanted to include low cloud, very low cloud, medium cloud and high cloud we could have the following query



<pre>

begin

item = 202

section = 9

end

begin

item = 203

section = 9

end

begin

item = 204

section = 9

end

begin

item = 205

section = 9

end

</pre>



In query files whitespace is ignored, # is used for comments and you can use the usual logical operators (> <= etc). You can also specify that at item must be one of a list via attr = (val1, val2, val3) and other more complex syntaxes - see the mass documentation linked at the top of this section for details.



## Editing or using alternate source code


If you want to use some different UM source code or make changes to the source code then you must tell rose to use that code instead and you must download it from the repo to edit it. If you go to https://code.metoffice.gov.uk/trac/um/browser, (the username and password are the MOSRS ones, if you can’t remember them your password is the same one you have to cache when you log into xvmsrose, and the username is the name it uses when it says hello after you cache your password) you can view the main UM source code (called the trunk) and everyone’s edits (called the branches).

The trunk code is under main->trunk and people’s individual branches are under main->branches->dev->username, or main->branches->pkg->username. You can go all the way down the tree to see each file with the comments and author for the latest commit.  Revision numbers are unique across all the source tree so you can also enter a revision number in the search box to view a the state of all branches at a current point in time.

On Monsoon you access the repos with a fcm url. For the UM there are two repositories of note. The first is the read write MOSRS repo which starts fcm:um.x_br, the second is the Puma read only mirror, which you can also access from Monsoon which begins fcm:um.xm_br. Note the addition of an m in the Puma url for mirror. IMPORTANT the Puma mirror is read only so you can checkout/download from it but you cannot create new branches on it. If you want to create a new branch you must use the MOSRS repo.

If all you wish to do is run some existing branch that already exists then go to the Rose GUI and go to fcm_make->env->Source and change um_sources to the branch you want. The path will be fcm:um.xm_br/<everything after main/branches on the code web page>. For example 

<pre>

fcm:um.xm_br/pkg/jonathanwilkinson/vn10.3_CASIM_super_v3_nostub

</pre>



Then also change the config_revision to @<revision_number>, for example @15118. 

If you want to make edits then you need to first create a new branch of your own based, then download it to your home directory, make the edits and commit them back to the repository. If you wish to start with the trunk code then to create a branch do

<pre>

fcm branch-create mybranch fcm:um.x_tr

</pre>



Alternatively if you wish to start with somebody else’s branch then do

<pre>

fcm branch-create --bob myTestBranch fcm:um.x_br/pkg/jonathanwilkinson/vn10.3_CASIM_super_v3_nostub@15118

</pre>



The --bob means branch of a branch. If you don’t include it then you will end up with the trunk and I think the revision number at the end is ignored. Note that when you use --bob the revision number of the last change of the branch that you are branching from is prepended to your branch name. Check the repository browser to check what the name is. For example if your branch name ends up being r4386_myAmazingModifications, then it means the last change in the branch you branched from occurred at revision 4386. You may well wish to find the revision number of the tip of your branch to enter it into rose. To do this do

<pre>

fcm info <branch_url>

</pre>



or if you have checked out the source you can do this in the source directory and omit the url.

Note that you must use the MOSRS repo (x_br, not xm_br) when creating a new branch. For those interested in svn, fcm:um.xm_br points to the subversion repository svn://puma.nerc.ac.uk/um.xm_svn/main/branches which is a read only mirror of the MOSRS branch. Once you have created your branch you will be able to see it on the code.metoffice.gov web page under the branches/dev section. Now you can download the new branch (or if you didn’t want to create your own branch then you can use this to download someone else’s branch)

fcm checkout fcm:um.x_br/dev/<mosrs_username>/myTestBranch



This will create a directory in your current working directory with the same name as the branch - in this case r328_precip_and_substep - and it will download the source code for that branch into it.

You can then edit the code as you wish. If the branch is your own then you should commit changes back to the repository. Do this as you complete specific small bits of work rather than just doing it at the end of every day. Do it often. When you do a commit you will be presented with a text editor to describe your changes. Be thorough and make sure the comments will make sense to others. The commit command should be executed from within the directory that fcm checkout created and looks like

<pre>

fcm commit

</pre> 



The joy of doing regular commits based around specific pieces of work is that if you mess things up you can go undo changes by checking out a different commit. 

You can find further descriptions of the fcm system at http://collab.metoffice.gov.uk/twiki/pub/Support/FCM/doc/user_guide/getting_started.html


## CASIM

CASIM is a cloud aerosol interaction scheme. It replaces the large scale precipitation part of the UM and does some other stuff as well, such as disable the cloud scheme. The code is hosted in the MONC MOSRS repository which you can browse at https://code.metoffice.gov.uk/trac/monc/browser. To use it with the UM you must use a UM branch which has the appropriate connecting code. The appropriate branches to use are documented at https://code.metoffice.gov.uk/trac/um/wiki/ticket/717/CASIM/package_branches. On that web page the Branch and Working revisions refer to the UM code and the CASIM revision refers to the CASIM branch hosted as part of MONC. Because it is hosted as part of MONC, the FCM url of the CASIM branch has the prefix fcm:casim.xm_br.



To use casim, copy an existing working job and use that as a starting point. Speak to Paul Field or Daniel Grosvenor about the latest CASIM suite to use.

If you wish to use a different branch to the one in the copied suite then this can be changed in the Rose GUI at fcm_make->env. Remember the change of branch prefix noted above. You can and should checkout a copy of the CASIM branch as there are some switches that you will need to change in the source code. You can either create a new branch or checkout an existing branch and change the flags and point Rose to the source directory. I would however, recommend creating a new branch and committing your flags, then specify the revision number in your Rose suite. You then have a record of exactly how your flags were set for a run.

You can create a branch the same way as the standard UM, but again note the url change above and remember to use x_br, not xm_br.



Some CASIM options can be set in Rose, others must be changed in the source code.



On Rose go to UM->namelist->UM Science Settings->Section 04 Microphysics (Large-scale precipitation). The CASIM variables are all at the top level.

<pre>

• l_rain - this is microphysics wide. It turns of all large scale precipitation regardless of CASIM.

• i_mcr_iter - This allows you to do extra CASIM steps per UM model step. You probably don’t need this unless you suspect you have a particular problem.

• l_mcr_qrain - setting this false switches off rain. If you switch this off you should probably switch off l_mcr_qgraup as well to avoid melting graupel creating rain. This is because the array elements that hold the rain are not allocated if this switch is false so it wil probably crash your model.

• l_mcrqgraup - set to false to switch off graupel

• precip_segment_size

• casim_aerosol_choice - Flag to say what CASIM should simulate. 0=no aerosol (CASIM does nothing), 1=liquid, ice and aerosol number, 2=liquid, ice and no aerosol, 3=liquid, ice and insoluble aerosol number, 4=everything. If you are doing cloud aerosol work use 4. Not sure I have this quite right, see the UM source code from a CASIM branch, file src/atmosphere/large_scale_precipitation/CASIM/casim_set_dependent_switches_mod.F90

• casim_aerosol_couple_choice - 0=fixed aerosol, 1=namelist specified in casim_aerosol_nml, 2=ancilliaries (i.e. climatography), 4=UKCA 1-way, 5=UKCA 2-way. In general only 1 is used. Speak to the code owner before using anything else.

• casim_moments_choice. A flag to set how many moments to use for each hydrometeor category (see below).

</pre> 

<pre>

casim_moments_choice Cloud moments Rain moments Ice moments Snow moments Graupel moments

0 1 1 1 1 1

1 2 2 2 2 2

2 2 3 0 0 0

3 1 2 0 0 0

4 1 1 0 0 0

5 1 3 0 0 0

6 2 2 0 0 0

7 2 2 2 2 0

8 2 3 2 3 3

</pre>



8 is the one most people are using. Note that 2-6 cause l_casim_warm_only to be set to true and if you use 2-6 you must set l_warm to true in mphys_switches.F90 (see below).



<pre>

• l_casim - switch casim on and off. If true then requires l_casim_bl to be set true.

• l_casim_bl - switch the casim boundary layer on. Most importantly this disables the UM cloud scheme by setting the critical relative humidity for cloud formation to 100%. This is because CASIM does not work with the standard UM cloud scheme. This can be switched on with l_casim switched off for testing.

In addition the following switches can be set in the casim source code. This is in the CASIM branch, not the UM branch with the casim lnkage code. The file to look at is src /mphys_switches.F90. You will probably want to change at least aerosol_option and iopt_act because the current 10.3 version of this file uses fixed cloud with no aerosol.

• l_warm - set to true to disable ice processes. If you do this then there will be an error thrown, however, it is thought that this is actually safe so you can just comment out the if statement that does the check. I’m not sure what happens if you use this and an incompatible casim_moments_choice.

• L_inuc. If you set this to true then it ignores the parameterization given in iop_inuc and does not nucleate ice. That said there is still a parameterization to create large ice or snow or something.

• l_hallet_mossop - turn Halet Mossop on/off.

• l_p* - various processes which you can turn on or off as you wish

• l_tidy_negonly - There is a tidy routine which deals with negative and small values of condensate. If l_tidy_negonly is set to true then this only tidies negative values of condensate, otherwise it tidies anything below a threshold.

• l_tidy_conserve_* - When removing condensate in the tidy routines energy and water are not conserved unless these variables are set to true.

• l_separate_rain - Track aerosol in Rain separately to cloud. Otherwise it is just tracked in water as a whole.

• l_process - Don’t change this, it is set by the code depending upon your value for l_process_level. 

• l_process_level - 0=no processing, 1= aerosol will be advected, captured in cloud/precip and when hydrometeors evaporate it will be released with the same size distribution that went in, 2=like 1 but when aerosol are released from hydrometeors they are aggregated so can move to bigger diameter modes, 3=like 1 for aerosol in ice and like 2 for aerosol in liquid. It is recommended to not use 2 as there is uncertainty about how ice modifies aerosol distributions.

• iopt_act - set whether to use the CASIM aerosol as CCN. 0=fixed number of CCN (i.e. don’t use CASIM aerosol), 1=use 90% of total aerosol as CCN, 2=use Twomey parameterisation to derive number of CCN, 3=use Abdul-Razzak & Ghan parameterisation to derive number of CCN. 2 and 3 are essentially based on the Kohler curve. 3 was the one recommended to me.

</pre>



## Admin Stuff


Of course once you have everything running you will have to deal with disks and storage and things. A useful  command which needs to be run on xcm is

<pre>

lfs quota -g <project> /work

</pre>



Which tells you how much space you are using. Obviously replace <project> with your project. Also this web page shows a daily summary of all projects http://collab.metoffice.gov.uk/twiki/bin/viewfile/Static/SystemMonitoring/Reports/latest_quota_report.txt



You may also want to know how much of your CPU allowance you have used up. You can check this at http://collab.metoffice.gov.uk/twiki/bin/viewfile/Static/SystemMonitoring/Reports/HPC_llfs.txt.



## Some example errors


Warning in umPrintMgr: umPrintLoadOptions : Failed to get filename for IO control file from environment

Warning in umPrintMgr: umPrintSetLevel : Problem reading 

forrtl: severe (18): too many values for NAMELIST variable, unit 10, file /work/projects/dacciwa/prosen/cylc-run/u-ac194/work/20140710T0000Z/DACCIWA_4km_dacciwa_control_4km_um_frame_000/input.nl, line 68, position 78

Image              PC                Routine            Line        Source             

um-createbc.exe    00000000005EA997  Unknown               Unknown  Unknown

um-createbc.exe    000000000061433A  Unknown               Unknown  Unknown

um-createbc.exe    00000000005003E0  lbc_grid_namelist         138  lbc_grid_namelist_file_mod.f90

um-createbc.exe    0000000000401B19  MAIN__                    178  createbc.f90

um-createbc.exe    000000000040050E  Unknown               Unknown  Unknown

um-createbc.exe    00000000006BEEF1  Unknown               Unknown  Unknown

um-createbc.exe    00000000004003E9  Unknown               Unknown  Unknown

[FAIL] um-createbc.exe input.nl # return-code=18

Received signal ERR

cylc (scheduler - 2016-02-29T12:11:56Z): CRITICAL Task job script received signal ERR at 2016-02-29T12:11:56Z

cylc (scheduler - 2016-02-29T12:11:56Z): CRITICAL DACCIWA_4km_dacciwa_control_4km_um_frame_000.20140710T0000Z failed at 2016-02-29T12:11:56Z

This error occurred in the “frame” job for my nested domain. Fixed it by rebuilding the executables and running rose suite-run --new. Not sure what the cause was.



### NaNs


Runtime Errors about nans often mean that your model has gone unstable. Have a look at the crashed crun’s job.out and you will see the peak vertical wind for each timestep. Check if this has suddenly increased at the last timestep that ran and check that it is at a sensible heigt (e.g. 10 m/s on model level 1 would be bad).

To solve it try reducing the timestep. Don’t forget to increase the requested wallclock time an/or number of processors to ensure you don’t run out of time.



### Fcm_make errors


If the first “bubble” of the fcm make fails then this means the extract has failed. Check your sources and make sure the fcm urls are correct. Also it might be worth checking them in the roses/<suite_id>/ap/fcm_make/rose-app.conf file directly as in the Rose GUI I had a path that I had accidentally pasted some stuff on the end with spaces in and this didn’t seem to show up in the GUI.



### Locked out of suite


Could not do rose sgc (error about connecting), rose suite-run --restart (error about suite running) or rose suite-sutdown (error about connecting). Qstat showed no jobs running or submitted.

To fix this do 

<pre>

ssh exvmscylc

ps aux | grep <username> #this lists all processes for you

                         #find those (if any) that are cylc

                         #related and note the pid for the

                         #kill commands below

kill <pid_1>

kill <pid_2>

…

exit                    #to exvmsrose

cd ~/roses/<suite_id>

rose suite-run --restart #This will error but

                         #note the ~/<username>/.cylc/ports

                         #file name for rm command below

rm <ports_file>

</pre>



### Error when creating a branch with FCM


If you cannot create a branch when using fcm, but you can do other things then check your source branch is from a writeable repository - the new branch is created in the same repository as the one you are copying from. The Puma mirrors (beginning fcm:um.xm_br are read only, if you try to create a branch from these fcm will try to create a branch on Puma, which will fail. It then asks for a password showing your Monsoon username, not your MOSRS one and then that will fail, then it asks for a username and password. This will also fail. To fix this use the equivalent MOSRS branch for a source which will be the same url, but will begin fcm:um.x_br.



### Global Run or Global Reconfiguration Run Out of Wallclock Time


These cannot be edited in rose - you must manually edit the file which sets them, see Wallclock Time section. 


