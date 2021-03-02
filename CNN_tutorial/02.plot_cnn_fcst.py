import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

# main derectory
main_dir = '/home/wei/tutorial/'

# load obs [40]
f = Dataset(main_dir+'data/godas_label_DJF_1980-2019.nc', 'r')
obs = f['nino'][:,0,0,0]
f.close()

# load cnn forecast [40]
f = Dataset(main_dir+'output/cnn/fcst.nc', 'r')
cnn = f['nino'][:,0,0,0]
f.close()

# skill
cor = np.round(np.corrcoef(obs, cnn)[0,1], 2)
rmse = np.round(np.sqrt(np.mean((obs - cnn) ** 2)), 2)

print('Correlation: '+str(cor))
print('RMSE: '+str(rmse))

#==========================================
# plot
#==========================================
# set figure size
plt.rcParams["figure.figsize"] = [6.4, 4.0]

# set x (time)
x = np.arange(40)

# obs
line1 = plt.plot(x, obs, 'black')
plt.setp(line1,linewidth=1.6, marker='o', markersize=0)

# cnn
line2 = plt.plot(x, cnn, 'orangered')
plt.setp(line2,linewidth=1.6, marker='o', markersize=3.0)

# set x-, y-axis
plt.xticks(np.arange(0,39,5), np.arange(1980,2019,5))
plt.tick_params(labelsize=7,direction='in',length=3,width=0.4,color='black')

# zero line
plt.axhline(0,color='black',linewidth=0.5)

# x-, y-label
plt.xlabel('Year', fontsize=8)
plt.ylabel('Nino3.4 (°C)', fontsize=8)
plt.title('6-month lead forecast for DJF Nino3.4', y=0.99, fontsize=9)

# legend
plt.legend(
    ['OBS', 'CNN (Cor='+str(cor)+', RMSE='+str(rmse)+')'], 
    loc='upper left', 
    prop={'size':7}, 
    ncol=2
    )

# set plot area
plt.subplots_adjust(bottom=0.1, top=0.93, left=0.1, right=0.96)

# save
plt.savefig(main_dir+'fig/result_cnn.png', dpi=300)
plt.close()

