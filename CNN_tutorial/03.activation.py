#!/usr/bin/env python
# Generate activation map (based on element-wise activation)
#JHK
import numpy as np
from netCDF4 import Dataset
import tensorflow as tf
from tensorflow import keras
from contextlib import redirect_stdout
import os

# ignore warning message
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

#===================================================================================
# gpu setting
#===================================================================================
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]= '3'
gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)

# main derectory
main_dir = '/home/wei/tutorial/'
 
#===================================================================================
# read test set (GODAS)
#===================================================================================
# input
f = Dataset(main_dir+'data/godas_input_MJJ_1980-2019.nc','r')
sst = f.variables['sst'][:]
t300 = f.variables['t300'][:]
f.close()

# merging [40,6,24,72]
test_x = np.append(sst, t300, axis=1)
del sst, t300

# axes swap [40,6,24,72] -> [40,72,24,6]
test_x = np.swapaxes(test_x, 1, 3)
test_tdim, xdim, ydim, zdim = test_x.shape

#===================================================================================
# load model
#===================================================================================
model = keras.models.load_model(main_dir+'output/cnn/model_last.hdf5')

#===================================================================================
# activation
#===================================================================================
conv1 = model.layers[1](test_x)
max1 = model.layers[2](conv1)
conv2 = model.layers[3](max1)
max2 = model.layers[4](conv2)

# [tdim,18,6,30]
conv3= np.array(model.layers[5](max2))

# [18*6*30,30]
w1 = np.array(model.layers[7].get_weights()[0])

# [30]
b1 = np.array(model.layers[7].get_weights()[1])

# [30,1]
w2 = np.array(model.layers[8].get_weights()[0])

# [1]
b2 = np.array(model.layers[8].get_weights()[1])

#===================================================================================
# dimension extension for element-wise muliplication
#===================================================================================
# conv3 [tdim,18,6,35] -> [tdim,18,6,35,50]
conv3 = conv3.reshape(test_tdim, 18, 6, 35, 1)
conv3 = np.repeat(conv3, 50, axis=4)

# w1 [18*6*35,50] -> [tdim,18,6,35,50]
w1 = w1.reshape(1,18,6,35,50)
w1 = np.repeat(w1, test_tdim, axis=0)

# b1 [50] -> [tdim,18,6,50]
b1 = b1.reshape(1,1,1,50)
b1 = np.repeat(b1,test_tdim,axis=0)
b1 = np.repeat(b1,18,axis=1)
b1 = np.repeat(b1,6,axis=2)
b1 /= (18 * 6)

# w2 [50,1] -> [tdim,18,6,50]
w2 = w2.reshape(1,1,1,50)
w2 = np.repeat(w2,test_tdim,axis=0)
w2 = np.repeat(w2,18,axis=1)
w2 = np.repeat(w2,6,axis=2)

# b2 [1] -> [tdim,18,6]
b2 = b2.reshape(1,1,1)
b2 = np.repeat(b2,test_tdim,axis=0)
b2 = np.repeat(b2,18,axis=1)
b2 = np.repeat(b2,6,axis=2)
b2 /= (18 * 6)

#====================================================================================
# generate activation map
#====================================================================================
# FC1 [tdim,18,6,35]
fc1 = np.tanh(np.sum(conv3 * w1, axis=3) + b1) 

# output [tdim,18,6]
activation = np.sum(fc1 * w2, axis=3) + b2

# [tdim,18,6] -> [tdim,6,18]
activation = np.swapaxes(activation, 1, 2)

#===================================================================================
# save
#===================================================================================
activation = np.array(activation)
activation.astype('float32').tofile(main_dir+'output/cnn/activation.gdat')

f = open(main_dir+'output/cnn/activation.ctl','w')
f.write('dset ^activation.gdat\n')
f.write('undef -9.99e+08\n')
f.write('xdef  18  linear   0.  20\n')
f.write('ydef   6  linear -55.  20\n')
f.write('zdef   1  linear 1 1\n')
f.write('tdef '+str(test_tdim)+'  linear jan1980 1yr\n')
f.write('vars   1\n')
f.write('act    1   1  activtion\n')
f.write('ENDVARS\n')
f.close()

os.system('cdo -f nc import_binary '+main_dir+'output/cnn/activation.ctl '+main_dir+'output/cnn/activation.nc')
os.system('rm -f '+main_dir+'output/cnn/activation.ctl '+main_dir+'output/cnn/activation.gdat')

