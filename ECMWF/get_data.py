#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
..moduleauthor: Helen (CEMAC)
    Adapted from dreambooker.site initializing UM from ERA5
..description: Download fields on model levels.
    :copyright: © 2019 University of Leeds.
..usage:
    python get_era5.sh 20181125 --N 90 --W 180 --S -90 --E -180 &
..args: START, END, North, West, Sout, East
..Requirements: cdsapi, grib_api, credentials for cds
            [cds api intructions](https://cds.climate.copernicus.eu/api-how-to)
"""
import cdsapi
import argparse
hstring = ("Date string, format YYYYMMDD")
hstring2 = ("North, South, East, West values")
parser = argparse.ArgumentParser()
parser.add_argument("date1", help=hstring, type=str)
parser.add_argument("--N", help=hstring2, type=str)
parser.add_argument("--S", help=hstring2, type=str)
parser.add_argument("--E", help=hstring2, type=str)
parser.add_argument("--W", help=hstring2, type=str)
args = parser.parse_args()
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete', {
    'class': 'od',
    'date': str(args.date1),
    'area': str(args.N) + '/' + str(args.W) + '/' + str(args.S) + '/' + str(args.E),
    'expver': '1',
    'levelist': '1/to/137',
    'levtype': 'ml',
    'param': '130.128/133.128/131.128/132.128',
    'stream': 'oper',
    'time': '00:00:00',
    'type': 'an',
    'grid': "0.25/0.25",
}, 'ec_grib_'+str(args.date1)+ '0000.anal')
