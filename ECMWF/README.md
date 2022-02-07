# USING ECMWF DATA

## Obtaining ECMWF data

### via cdsapi on ARCHER

1. register at [https://cds.climate.copernicus.eu](https://cds.climate.copernicus.eu)
2. obtain your UID and API Key from your profile page
3. create a file `~/.cdsapirc` on ARCHER with this content
```
url: https://cds.climate.copernicus.eu/api/v2
key: <UID>:<API KEY>
```
4. set up environment
`module load cray pythong`
`pip install --user ecmwf-api-client`
`pip install --user cdsapi`
5. Run script `get_data.py`

## Run model

* run `make ancils only` with extra domain, larger than your domain 1
* store these ancillaries
* you may need to edit `meta/rose-meta.conf` to allow more domains if you're already using 5 and run `/bin/setup_metadata` to generate a new file **NB** backup your suite.rc and conf files.
* run the model with `Driving model` set to ECMWF (point to ancils generated and the grib files)

## Modifying a suite/um code to use ECMWF data

The UM executable needs to know about eccodes in order to decode girb files

You will need to use a version of the UM that allows this in both the fcm config and source
in the rose suite point to the correct code

`fcm_make`--> `Configuration file` --> `config_root_path` : `fcm:um.x_br/dev/helenburns/r93258_vn11.1_archer2_compile_eccodes`

and source

`fcm_make`--> `Sources` --> `um_sources` : `fcm:um.x_br/dev/helenburns/11.4_11.4_GRIB_API`

in these branches I have edited
`external_paths.cfg` `parallel.cfg` `rcf_grib_block_params_mod.F90` and `ukmo_grib_mod.F90`

to allow eccodes to be used.

# Building eccodes

[Offical Eccode installation notes](https://confluence.ecmwf.int/display/ECC/ecCodes+installation)

```bash
mkdir eccodes
`wget https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.22.0-Source.tar.gz`
tar -xvf eccodes-2.22.0-Source.tar.gz
mkdir build
cd build
```

make sure the correct modules are loaded. These need to match what is loaded when um is loaded

```bash
module load cmake
module load cce/12.0.3
module load cray-hdf5
module load cray-netcdf

```

The following flags are required

```
cmake <path-to-source> -DCMAKE_INSTALL_PREFIX=<path-to-install-dir> -DBUILD_SHARED_LIBS=OFF -DENABLE_JPG=OFF
```

Here's a example of my debugging cmake command adding extra tests and -g flag

```
cmake  ../eccodes-2.22.0-Source -DCMAKE_INSTALL_PREFIX=/work/n02/n02/hburns/eccodes/2.22.0 -DENABLE_EXTRA_TESTS=ON  -DCMAKE_Fortran_COMPILER=ftn -DCMAKE_Fortran_FLAGS=-g -DBUILD_SHARED_LIBS=OFF -DENABLE_JPG=OFF
```


There's a bug in the ftn wrapper here RUNPATH does not get set properly
Need to explicitly add path to location of libunwind.so to link line before running make
Edit fortran/CMakeFiles/grib_types.dir/link.txt to replace ``-Wl,rpath`, setting with:

`-Wl,rpath,/opt/cray/pe/cce/12.0.3/cce-clang/x86_64/lib/libunwind.so`

in the following files

```
fortran/CMakeFiles/grib_types.dir/link.txt
examples/F90/CMakeFiles/eccodes_f_grib_ecc-671.dir/link.txt
examples/F90/CMakeFiles/eccodes_f_grib_set_data.dir/link.txt
examples/F90/CMakeFiles/eccodes_f_grib_set_pv.dir/link.txt
```

once those edits are made you can finish the rest of the installation 

```
make -j4
ctest -j4
make install
```
