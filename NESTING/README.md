# Nesting

An example nesting suite can be found.

# Adjusting domains


# Rotating Poles

To make diagonal boxes you can rotate poles to reduce number of grid points required.

## Locating poles

Using LAMPOS on puma

create a lampos file in bin folder:
```bash
#! /bin/sh
exec /usr/bin/wish -f /home/umui/lamposvn4.2/lampos.tcl
```

running this will create a GUI where you can play around with location of poles
and will get a lat lon of lower lefthand corner.

Modern UM requires a center point so you will be to calculate the center lat long

## Setting the suite to use rotated poles

1. In Nested Region 1 set `rg01_rot_grid` to `TRUE`
2. go to `UM` --> `namelist` --> `LAM Configuration` and set your pole information obtained from lampos
