#!/usr/bin/env python3
'''
Download hourly data for ML workflow per year 
from https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5

can monitor queue here https://cds.climate.copernicus.eu/live/queue 
and details on limits https://cds.climate.copernicus.eu/live/limits
The maximum number of per-user requests that access the online CDS data is 3

1 level cap hourly , 15 min to process and download
10 pressure levels hourly ~521MB, ~2hours to processes request and download
for nightly runs, not a big deal GitHub Actions Workflow run time - Each workflow run is limited to 72 hours.

CRS info: https://confluence.ecmwf.int/display/CKB/ERA5%3A+What+is+the+spatial+reference

Usage: get_era_data.py 2017
'''
import sys
import os
import cdsapi

# set up client connection assumes ~/.cdsapirc 
# can also directly pass credentials w/ cdsapi.Client(url='xxx',key='xxx:xxx')
c = cdsapi.Client()

# common request parameters
request_template = dict(
    product_type='reanalysis',
    variable=None,
    year=None,
    #month = [f'{n:02}' for n in range(1,13)],  # all months                  Default: all months
    #day = [f'{n:02}' for n in range(1,32)],    # all days                    Default: all days
    time = [f'{n:02}:00' for n in range(24)],   # every hour.                 Default: per day
    area=[60, -135, 20, -60],                  # North, West, South, East.   Default: global
    grid=[1.0, 1.0],                          # Latitude/longitude grid.    Default: 0.25 x 0.25.
    format='netcdf',
)

# native grid resolution depends on product type it seems
#Please note that the ERA5 native grid of online CDS is 0.25°x0.25° (atmosphere), 0.5°x0.5° (ocean waves), mean, spread and members: 0.5°x0.5° (atmosphere), #1°x1° (ocean waves). ERA5-Land: 0.1°x0.1°. So this will be returned by default.

def make_request_dictionary(template, template_updates):
    request_params = request_template.copy()
    request_params.update(template_updates)
    
    return request_params


def retrive_single_level(request):
    outfile = 'ERA_{year}_{variable}.nc'.format(**request)
    if os.path.exists(outfile):
        print(f'{outfile} exists, skipping')
        return
    
    print(f'downloading {var} for {year}...')
    c.retrieve('reanalysis-era5-single-levels', request_params, outfile)
    
    
def download_sequential(year):
    print('\n\nDownloading...\nvisit https://cds.climate.copernicus.eu/live/queue to monitor\n\n')

    single_vars = ['convective_available_potential_energy']
    
    for var in single_vars:
        request = make_request_dictionary(request_template, dict(year=year, var=var))
        print(outfile, request)
        retrieve_single_level(request, outfile)
    
    
# Quick experiment with parallel downloads
def retrieve_pressure_levels(request):
    outfile = 'ERA_{year}_{variable}.nc'.format(**request)
    if os.path.exists(outfile):
        print(f'{outfile} exists, skipping')
    else:
        c.retrieve('reanalysis-era5-pressure-levels', request, outfile)  
    
    
def download_pressure_levels(year):
    ''' use parallel processing to download pressure levels because it takes > 1hr to download... '''
    # https://stackoverflow.com/questions/34031681/passing-kwargs-with-multiprocessing-pool-map
    # NOTES: 10 pressure levels hourly ~521MB, ~2hours to processes request and download
    
    import multiprocessing
    
    pressure_vars = ['geopotential',
                     'specific_humidity',
                     'temperature',
                     'u_component_of_wind',
                     'v_component_of_wind'] 
    
    requests = []
    for var in pressure_vars:
        update_params = dict(year=year,
                             variable=var,
                             pressure_level=[f'{n}00' for n in range(1,11)], # 100
                            )
        
        request = make_request_dictionary(request_template, update_params)
        requests.append(make_request_dictionary(request_template, update_params))      
    
    #nproc = 3 # cdsapi per-user limit
    nproc = len(requests)
    pool = multiprocessing.Pool(processes=nproc)
    pool.map(retrieve_pressure_levels, requests)
    

if __name__ == "__main__":
    year = sys.argv[1]
    #download_single_level(year)
    download_pressure_levels(year)