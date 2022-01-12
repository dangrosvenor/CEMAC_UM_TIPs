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

### Trouble shutting down a suite

```bash
ps -flu <username> | grep <suite-id>
```

then you can `kill -9 <PID>` the process that is still running preventing the suite from shutting down

# Debugging tips

if the job.err messages are completely unhelpful there's a number of things you can do.

1. Try running: `addr2line --exe=</path/too/executable> <address>`
2. Rerun in debug mode

in *site/<HOST_HPC>/suite-adds.rc* add
  ```bash
  module load atp
  export ATP_ENABLED=1
  ```
  to the `HOST_HPC init-script`

  **AND**

  switching on extra output by

  *um > env > runtime controls > atmosphere only* set PRINT_STATUS to "Extra diagnostic messages"

a similar thing can be done if your issue is in recon step
