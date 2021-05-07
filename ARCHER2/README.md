# ARCHER with 2FA FROM PUMA

These are some tips for transfering from ARCHER to ARCHER 2 (access via PUMA)

## information

NCAS CMS have some usefull information on how to modify your suite.



* LINUX must be set to background (from at)
* site/archer.rc and ncas_cray  might be required to run

### Met office password cahce
`mosrs-cache-password `

### Permission errors
```
rm -f  ~/.ssh/environment.puma
eval `ssh-agent -s`
ssh-add -D
ssh-add ~/.ssh/id_rsa_archerum
```
weird FCM make permission error... not always ? Sometimes runs fine ?


# ARCHER 2 Pilot scheme

[CMS UM on archer 2 pages](http://cms.ncas.ac.uk/wiki/Archer2#UM)

Note nothing will work out of the box.

1. Follow on boarding instructions
2. run example suite
  1. ~/.bash_profile  edit on ARCHER 2
  2. edit or add `site/archer2.rc` type file or `site/ncas_cray_ex/suite-adds.rc`
      * `--chdir=/work/n02/n02/<your ARCHER2 user name>`  line must be edited

# SLURM COMMANDS

* `sinfo`  information on nodes available
* `squeue -l | grep $USER` check if your jobs are running
* `squeue -l | grep PENDING | wc -l` how long is the queue
* `squeue -R shortqos` check the short queue

# Gotchas

* WALLCLOCK LIMIT is in minutes not seconds there 60 is 1 hour not 1 min
this can be fixed editing `bin/setup_metadata`
```
fp.write("WALL_CLOCK_LIMIT=20\n")
fp.write("range=1:172800\n")
```
and `meta/rose-meta.conf` swapping `range=60:172800` to `range=1:172800`
* Node is 8x8 CPUS (actually 128 cores as hyper threaded)
* Python mismatches - if loading in cray-python must load after other cyclc tasks and unload in after in pre scripts
* Nesting Suite archer suite had reference to short partition which does not exist short q is accessed by short reservation on standard partition
* short q limited to 1 running 1 queuing
*

### Troubleshooting:

1. Access issue
 `ssh login.archer2.ac.uk`

 returns

 `PTY allocation request failed on channel 0`
 `bash: /home1/z00/puma-access-route/bin/pumawrapper: No such file or
 directory`

check the path in

 `/home1/system/puma-access-route/keys/$USER`

 `/home1/z00/` should be `/home1/system/`
