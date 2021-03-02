import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# main derectory
main_dir = '/home/wei/tutorial/'

# target year
yr = 1997

# set title
if yr < 2000:
  ts = yr - 1900
else:
  ts = yr - 2000
tn = ts+1
tit = str(ts)+'/'+str(tn)
del ts, tn

# read activation map [40,6,18]
f = Dataset(main_dir+'output/cnn/activation.nc','r')
hm = f['act'][:,0]

# read observation [40,24,72]
f = Dataset(main_dir+'data/godas_input_MJJ_1980-2019.nc','r')
sst = f.variables['sst'][:,:,:,:]
hc  = f.variables['t300'][:,:,:,:]

# MJJ mean
sst = np.mean(sst,axis=1)
hc  = np.mean(hc,axis=1)

# replace sst to hc for equatorial Pacific area (120-280E, 20S-20N)
def lon_to_xdim(lon_st, lon_nd, lon_int=2.5, lon_init=0.0):

  x_st = int( ( lon_st + lon_init ) / lon_int )
  x_nd = int( ( ( lon_nd + lon_init ) / lon_int ) + 1 )

  return x_st, x_nd

def lat_to_ydim(lat_st, lat_nd, lat_int=2.5, lat_init=-90.0):

  y_st = int( ( lat_st - lat_init ) / lat_int )
  y_nd = int( ( ( lat_nd - lat_init ) / lat_int ) + 1 )

  return y_st, y_nd

x_st, x_nd = lon_to_xdim(120,280,lon_int=5)
y_st, y_nd = lat_to_ydim(-20,20,lat_int=5)

sst[:,y_st:y_nd,x_st:x_nd] = hc[:,y_st:y_nd,x_st:x_nd]

#==========================================
# plot
#==========================================

# make x, y
x, y  = np.meshgrid(np.arange(0,360,5), np.arange(-57.5,62.5,5))

# contour (observation)
# positive contour line
CS = plt.contour(x,y,sst[yr-1980,:,:],np.arange(0.5,3.001,0.5),colors='black',linewidths=0.6, zorder=4)
plt.clabel(CS,fontsize=5, fmt='%1.1f',inline=True)
[txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0, alpha=0.7)) for txt in CS.labelTexts]

# negative contour line
CS = plt.contour(x,y,sst[yr-1980,:,:],np.arange(-3.0,0,0.5),colors='black',linewidths=0.6, zorder=4)
plt.clabel(CS,fontsize=5, fmt='%1.1f',inline=True)
[txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0, alpha=0.7)) for txt in CS.labelTexts]

for line in CS.collections:
  if line.get_linestyle() != [(None, None)]:
    line.set_linestyle([(0, (5, 3))])

# shading (activation)
cax = plt.imshow(hm[yr-1980,:,:], cmap='RdBu_r',clim=[-1.0,1.0],
                 extent=[0,360,60,-55],zorder=1)

# set map
map = Basemap(projection='cyl', llcrnrlat=-55,urcrnrlat=59, resolution='c',
              llcrnrlon=20, urcrnrlon=360)
map.drawparallels(np.arange( -90., 90.,30.),labels=[1,0,0,0],fontsize=6,
                  color='grey', linewidth=0.6)
map.drawmeridians(np.arange(0.,360.,30.),labels=[0,0,0,1],fontsize=6,
                  color='grey', linewidth=0.6)
map.fillcontinents(color='silver', zorder=3)

# plot equatorial Pacific as black thick line
x = [  120,   280,   280,   120,   120]
y = [  -20,   -20,    20,    20,   -20]
plt.plot(x,y,'black',zorder=4,linewidth=0.9)

# stitle
plt.title('6-month lead activation map for '+tit+' El Niño', x=0.5, y=0.97,
           fontsize=7, ha='center')

# colorbar
cax = plt.axes([0.05, 0.055, 0.9, 0.013])
cbar = plt.colorbar(cax=cax, orientation='horizontal')
cbar.ax.tick_params(labelsize=5.5,direction='out',length=2,width=0.4,color='black',zorder=6)



# set plot area
plt.subplots_adjust(bottom=0.08, top=0.55, left=0.05, right=0.95)

# save
plt.savefig(main_dir+'fig/activation.png', format='png', dpi=300)
plt.close()







