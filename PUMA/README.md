# PUMA tips


### Permission denied (publickey)

1. remove `~/.ssh/environment.puma`
2. remove any erroneous or old keys that might be getting picked up by accident
  * If you're unsure move them to a backup folder
4. log out and back in
3. run `ssh-add ~/.ssh/id_rsa_archerum`

If this happens regularly try running:

```bash
eval `ssh-agent -s`
ssh-add -D
ssh-add ~/.ssh/id_rsa_archerum
```

however if you having to do this something is wrong with your set up

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
