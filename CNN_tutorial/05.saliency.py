#!/usr/bin/env python
#JHK
import numpy as np
from netCDF4 import Dataset
import tensorflow as tf
from tensorflow import keras
from contextlib import redirect_stdout
import os, sys

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
# generate saliency map
#===================================================================================
sal_map = np.zeros((test_tdim,6,24,72))
for i in range(test_tdim):

    tmp = tf.Variable(np.array(test_x[i:i+1]), dtype=float)
    
    # compute gradient
    with tf.GradientTape() as tape:
        pred = model(tmp, training=False)[0] 
        grads = tape.gradient(pred, tmp)[0]
    
    # [xdim,ydim,zdim] -> [zdim,ydim,xdim]
    grads = np.swapaxes(grads, 0, 2)
    sal_map[i] = grads

#===================================================================================
# save
#===================================================================================
sal_map = np.array(sal_map)
sal_map.astype('float32').tofile(main_dir+'output/cnn/saliency.gdat')

ctl = open(main_dir+'output/cnn/saliency.ctl','w')
ctl.write('dset ^saliency.gdat\n')
ctl.write('undef -9.99e+08\n')
ctl.write('xdef  72  linear   0.  5\n')
ctl.write('ydef  24  linear -55.  5\n')
ctl.write('zdef   6  linear 1 1\n')
ctl.write('tdef '+str(test_tdim)+'  linear jan1980 1yr\n')
ctl.write('vars   1\n')
ctl.write('sal   6   1  saliency map\n')
ctl.write('ENDVARS\n')
ctl.close()

os.system('cdo -f nc import_binary '+main_dir+'output/cnn/saliency.ctl '+main_dir+'output/cnn/saliency.nc')
os.system('rm -f '+main_dir+'output/cnn/saliency.ctl '+main_dir+'output/cnn/saliency.gdat')

