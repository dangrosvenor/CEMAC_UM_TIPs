# PUMA tips

## GDK Display Errors

Check `quota` often these errors posing as display errors when launching rose GUIs appear due to lack of disk space

`du -sh`  in your home directory should reveal largest space drains. The default quota for Puma is 1GB

# Archer2 new 23 cabinet system

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

Now you should have no more mismatching keys

*NB only do this when you are expecting the keys to mismatch - otherwise a key mismatch could highlight something malicious*
