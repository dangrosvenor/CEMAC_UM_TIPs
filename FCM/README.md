# FCM Tips

### General

1. Create a ticket [here](https://code.metoffice.gov.uk/trac/um/newticket) *selecting not for builds if its just your personal work*
2. `fcm branch-create -k <ticket> <branch_name> fcm:um.x-tr@vn11.1` *links to your ticket and bracnhes from trunk at specified version*
3. `fcm checkout <url>` *checks out a working copy for you to edit*
4. `fcm commit` regularly to keep track of changes
5. `fcm diff` shows you your edits


### Others

Sometimes you want to create a branch of a branch. **NB** If you want to merge back into truck you must merge back into the original branch first

`fcm branch-create -k <ticket> <branch_name> --bob fcm:um.x-br/dev/<user>/<branchname>`

## Using FCM on ARCHER2

1. copy `~/.subversion/servers` from puma on archer2 to `~/.subversion/servers`
2. add `/work/y07/shared/umshared/bin/` to your path
3. run `. mosrs-setup-gpg-agent` # this will ask for you metoffice password
4. `mosrs-cache-password` will now chache you mosrs and allow fcm commands to run 
