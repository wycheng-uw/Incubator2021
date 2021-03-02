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
suptit = str(ts)+'/'+str(tn)
del ts, tn

# read saliency map [40,6,24,72]
f = Dataset(main_dir+'output/cnn/saliency.nc','r')
sal = f['sal'][:]

## normalize
#sal = sal / np.std(sal)
sal_std = np.std(sal.reshape(40,6,24*72), axis=2).reshape(40,6,1)
sal_std = np.repeat(sal_std, 24*72, axis=2).reshape(40,6,24,72)
sal /= sal_std

#np.flip(sal, axis=2)
#np.flip(sal, axis=3)

# read observation [40,6,24,72]
f = Dataset(main_dir+'data/godas_input_MJJ_1980-2019.nc','r')
sst = f.variables['sst'][:,:,:,:]  # [40,3,24,72]
hc  = f.variables['t300'][:,:,:,:] # [40,3,24,72]

# merging [40,6,24,72]
obs = np.append(sst, hc, axis=1)
del sst, hc

sal *= obs

#==========================================
# plot
#==========================================
# make x, y
x, y  = np.meshgrid(np.arange(0,360,5), np.arange(-57.5,62.5,5))

fig_num_list = [1, 3, 5, 2 ,4, 6]
tit_list = [
    '(a) May SST',
    '(b) Jun SST',
    '(c) Jul SST',
    '(d) May HC',
    '(e) Jun HC',
    '(f) Jul HC'
    ]

for i in range(6):

    fig_num = fig_num_list[i]
    tit = tit_list[i]
    plt.subplot(3,2,fig_num)

    # contour (observation)
    # positive contour line
    CS = plt.contour(x,y,obs[yr-1980,i,:,:],np.arange(0.5,3.001,0.5),colors='black',linewidths=0.6, zorder=4)
    plt.clabel(CS,fontsize=5, fmt='%1.1f',inline=True)
    [txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0, alpha=0.7)) for txt in CS.labelTexts]

    # negative contour line
    CS = plt.contour(x,y,obs[yr-1980,i,:,:],np.arange(-3.0,0,0.5),colors='black',linewidths=0.6, zorder=4)
    plt.clabel(CS,fontsize=5, fmt='%1.1f',inline=True)
    [txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0, alpha=0.7)) for txt in CS.labelTexts]

    for line in CS.collections:
        if line.get_linestyle() != [(None, None)]:
            line.set_linestyle([(0, (5, 3))])

    # shading (activation)
    cax = plt.imshow(sal[yr-1980,i,:,:], cmap='RdBu_r',clim=[-1,1],
                     extent=[0,360,60,-55],zorder=1)

    # set map
    map = Basemap(projection='cyl', llcrnrlat=-55,urcrnrlat=59, resolution='c',
                  llcrnrlon=20, urcrnrlon=360)
    map.drawparallels(np.arange( -90., 90.,15.),labels=[1,0,0,0],fontsize=6,
                      color='grey', linewidth=0.6)
    map.drawmeridians(np.arange(0.,380.,30.),labels=[0,0,0,1],fontsize=6,
                      color='grey', linewidth=0.6)
    #map.drawcoastlines(color='grey',linewidth=0.3)
    map.fillcontinents(color='silver', zorder=3)

    # title
    plt.title(tit, x=0.0, y=0.96,
               fontsize=7, ha='left')

    # colorbar
    cax = plt.axes([0.05, 0.055, 0.9, 0.013])
    cbar = plt.colorbar(cax=cax, orientation='horizontal')
    cbar.ax.tick_params(labelsize=5.5,direction='out',length=2,width=0.4,color='black',zorder=6)

plt.suptitle('Saliency map for '+suptit+' El Niño', fontsize=9)

plt.tight_layout(h_pad=1,w_pad=1)

# set plot area
plt.subplots_adjust(bottom=0.1, top=0.90, left=0.05, right=0.95)

# save
plt.savefig(main_dir+'fig/saliency.png', format='png', dpi=300)
plt.close()







