#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
..moduleauthor: Helen (CEMAC)
    Adapted from dreambooker.site initializing UM from ERA5
..description: Download fields on model levels.
    :copyright: © 2019 University of Leeds.
..usage:
    python get_era5.py 20181101 --t
..args: <date> YYYYMMDD --t <time-HH>
..Requirements: cdsapi, grib_api, credentials for cds
            [cds api intructions](https://cds.climate.copernicus.eu/api-how-to)
"""
import cdsapi
import argparse
from datetime import datetime, timedelta
hstring = ("Date string, format YYYYMMDD, -t HH hour")
parser = argparse.ArgumentParser()
parser.add_argument("date", help=hstring, type=str)
parser.add_argument("--t", help=hstring, type=str)
args = parser.parse_args()
# Extract YYYY, MM, DD and HH
t = args.t
year = args.date[0:4]
month = args.date[4:6]
day = args.date[-2::]
# if t is 24 then its 00 the next day
if t == 24:
    t = 00
    date=args.date
    date = datetime(int(year),int(month), int(day)) - timedelta(days=1)
    year = date.year
    month = date.month
    day = date.day
    
# Create api cliant
c = cdsapi.Client()

# Retrieve single level
# 'geopotential'
# 'land_sea_mask',
# 'skin_temperature',
# 'surface_pressure'
# 'soil_temperatures',
# 'soil_moistures',
# 'snow_density',
# 'snow_depth'

print('Retrieving ' + str(year) + str(month) + str(day) + ' ' + str(t) + ':00')
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'grib',
        'variable': [
            'geopotential', 'land_sea_mask', 'skin_temperature',
            'surface_pressure', 'soil_temperature_level_1', 'soil_temperature_level_2', 'soil_temperature_level_3',
            'soil_temperature_level_4', 'soil_type', 'volumetric_soil_water_layer_1',
            'volumetric_soil_water_layer_2', 'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4',
            'snow_density', 'snow_depth'
        ],
        'year': str(year),
        'month': str(month),
        'day': str(day),
        'time': str(t) + ':00',
    },
    'surfacelevels.grib')

# Retrieve Pressure level fields (all levels)
# 'specific_humidity',
# 'temperature',
# 'u_component_of_wind',
# 'v_component_of_wind'

c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type': 'reanalysis',
        'format': 'grib',
        'variable': [
            'specific_humidity', 'temperature', 'u_component_of_wind',
            'v_component_of_wind',
        ],
        'pressure_level': [
            '1', '2', '3',
            '5', '7', '10',
            '20', '30', '50',
            '70', '100', '125',
            '150', '175', '200',
            '225', '250', '300',
            '350', '400', '450',
            '500', '550', '600',
            '650', '700', '750',
            '775', '800', '825',
            '850', '875', '900',
            '925', '950', '975',
            '1000',
        ],
        'year': str(year),
        'month': str(month),
        'day': str(day),
        'time': str(t) + ':00',
    },
    'pressure.grib')
