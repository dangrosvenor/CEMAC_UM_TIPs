# PUMA tips

## Rose suite shutdown fail

Probably due to a local process:

`ps -flu <puma-user-name> | grep <suite-id>`

then kill the offending process with `kill -9 <pid>`

## re-accessing the cylc gui

* rose sgc

## Submit fail with no obvious error

Connection error with no permission/ pub- key or other recognisable error can be an intermittent connection drop and simply resolved by a resubmit

## GDK Display Errors

Check `quota` often these errors posing as display errors when launching rose GUIs appear due to lack of disk space

`du -sh`  in your home directory should reveal largest space drains. The default quota for Puma is 1GB

# Archer2 new 23 cabinet system


## Host Key verification failed / submit failed

`[FAIL] Host key verification failed.`

Occurs because Archer2 now has a different key the 4 cabinet system

`ssh-keygen -R login.archer2.ac.uk`

should resolve it

some users might need to check there's no other toublesome keys

`ssh -o BatchMode=yes -o StrictHostKeyChecking=no  login.archer2.ac.uk`
might pop up a warning:

`Warning: the ECDSA host key for 'login.archer2.ac.uk' differs from the key for the IP address '193.62.216.45'``

telling you the other offending key to remove e.g.:

`ssh-keygen -R 193.62.216.45`

Now you should have no more mismatching keys. (possibly you'll need to repeat this step a few times to cover all the ip addresses!)

*NB only do this when you are expecting the keys to mismatch - otherwise a key mismatch could highlight something malicious*

## Module fails

Job fails with error logs not finding modules

`module restore module` yields : `Lmod has detected the following error:  User module collection: "2020.12.14" does not exist.`

`module restore` is no longer a command. `module load um` will load um modules
