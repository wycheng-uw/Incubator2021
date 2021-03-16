import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4

path_to_output_files = '/home/disk/eos12/wycheng/data/GEFS/'

var_list = ['zg']

for var in var_list:
  url   = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.SubX/.EMC/.GEFS/.hindcast/."+var+"/dods"

  remote_data = xr.open_dataset(url,chunks={'S':'auto', 'P':'auto', 'M':'auto', 'L':'auto', 'Y':'auto','X':'auto'}, decode_times=False)

  data = remote_data[var].isel(S=slice(574,939),P=slice(0,2))

  data.to_netcdf(path_to_output_files+'GEFS_'+var+'.nc',mode='w')
