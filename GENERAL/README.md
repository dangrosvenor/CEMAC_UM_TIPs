# General UM notes

## CMS helpdesk

[new cms helpdesk website](https://cms-helpdesk.ncas.ac.uk/)

The [NCAS UM tutorial](http://cms.ncas.ac.uk/documents/training/November2019/)


## Check out a test suite

Suite `u-` should run on archer 2 with a swap of the charging code and user name

`Rosie go` search for suite and make a **copy**

`cd <suite-name>`
`rose edit`

make required edits user name and charging code and run  

# Running a Suite

in a suite dir run:

`rose suite-run new`

### Gotchas

### Permission denied (publickey)

Something is probably wrong with your setup if this happens regularly try running:

```bash
eval `ssh-agent -s`
ssh-add -D
ssh-add ~/.ssh/id_rsa_archerum
```
