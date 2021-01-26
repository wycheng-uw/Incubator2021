from mpl_toolkits.basemap import Basemap, cm
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.legend_handler import HandlerLine2D
from netCDF4 import Dataset

YYYYs = '2013'

nt, nlat, nlon  = (2920, 40, 75)
#nt, nlat, nlon  = (2928, 40, 75)

arrayo = np.zeros((nt,nlat,nlon))
arrayo[:,:,:] = np.nan

first_file = True;

#diri = '/home/disk/tc/msahn/OBS/msahn_snu/PRCP_trmm.3hour/'+YYYYs+'/'
diri = '/home/disk/tc/msahn/OBS/msahn_snu/PRCP_trmm.3hour/3B42_V7_old/'+YYYYs+'/'
fils = sorted(glob.glob(diri + '*.nc'))

datetime0 = datetime(int(YYYYs),  1,  1,  0, 0, 0, 0)

for filename in fils[:]:
    print(filename)
    
    MMs       = filename[76:78]
    DDs       = filename[78:80]
    hhs       = filename[81:83]
    datetime1 = datetime(int(YYYYs), int(MMs), int(DDs), int(hhs), 0, 0, 0)
    ihh       = int((datetime1-datetime0).total_seconds() // 3600)
    jhh       = int(ihh/3)
    print(jhh)
    
    ncin      = Dataset(filename,'r')

    if (first_file):
        lat_in      = ncin.variables['latitude'][:];
        lon_in      = ncin.variables['longitude'][:];
                
        first_file  = False
#    try:
    pcp_in    = ncin.variables['pcp'][0,:,:];
#    except:
#        continue
    
    for ilat in np.arange(110,150,1):
        for ilon in np.arange(45,120,1):
#            try:
            arrayo[jhh,ilat-110,ilon-45] = np.mean(pcp_in[(ilat-40)*4:(ilat-40)*4+4,(ilon)*4:(ilon)*4+4])
#            except:
#                continue

time_hh     = np.linspace(     0, nt-1,nt);
lat         = np.linspace(  20.5, 59.5,nlat);
lon         = np.linspace(-134.5,-60.5,nlon);

ncout   = Dataset('TRMM_'+YYYYs+'_pcp_cg_1deg3hr_US.nc','w','NETCDF4');
ncout.createDimension('time',nt);
ncout.createDimension('lat',nlat);
ncout.createDimension('lon',nlon);

lonvar  = ncout.createVariable('lon','float32',('lon'));lonvar[:] = lon;
latvar  = ncout.createVariable('lat','float32',('lat'));latvar[:] = lat;
timevar = ncout.createVariable('time','float32',('time'));timevar[:] = time_hh;

pcpvar  = ncout.createVariable('pcp',np.float32,('time','lat','lon'));

pcpvar[:,:,:] = arrayo[:,:,:];
                                   
ncout.close()
