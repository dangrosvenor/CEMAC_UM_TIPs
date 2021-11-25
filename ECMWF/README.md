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
* store these anciclaries
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
