#!/usr/bin/env python
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
# read train set (CMIP5)
#===================================================================================
# input
f = Dataset(main_dir+'data/cmip5_tr_input_MJJ_1861-2003.nc','r')
sst = f.variables['sst'][:]     # [3003,3,24,72]
t300 = f.variables['t300'][:]   # [3003,3,24,72]
f.close()

# merging [3003,6,24,72]
tr_x = np.append(sst, t300, axis=1)
del sst, t300

# axes swap [3003,6,24,72] -> [3003,72,24,6]
tr_x = np.swapaxes(tr_x, 1, 3)
tr_tdim, xdim, ydim, zdim = tr_x.shape

# label [3003,1]
f = Dataset(main_dir+'data/cmip5_tr_label_DJF_1861-2003.nc','r')
tr_y = f.variables['nino'][:,:,0,0]
f.close()

#===================================================================================
# read validation set (CMIP5)
#===================================================================================
# input
f = Dataset(main_dir+'data/cmip5_val_input_MJJ_1861-2003.nc','r')
sst = f.variables['sst'][:]    # [858,6,24,72]
t300 = f.variables['t300'][:]  # [858,6,24,72]
f.close()

# merging [858,6,24,72]
val_x = np.append(sst, t300, axis=1)
del sst, t300

# axes swap [858,6,24,72] -> [858,72,24,6]
val_x = np.swapaxes(val_x, 1, 3)
val_tdim, xdim, ydim, zdim = val_x.shape

# label [858,1]
f = Dataset(main_dir+'data/cmip5_val_label_DJF_1861-2003.nc','r')
val_y = f.variables['nino'][:,:,0,0]
f.close()

#===================================================================================
# read test set (GODAS)
#===================================================================================
# input
f = Dataset(main_dir+'data/godas_input_MJJ_1980-2019.nc','r')
sst = f.variables['sst'][:]    # [40,6,24,72]
t300 = f.variables['t300'][:]  # [40,6,24,72]
f.close()

# merging [40,6,24,72]
test_x = np.append(sst, t300, axis=1)
del sst, t300

# axes swap [40,6,24,72] -> [40,72,24,6]
test_x = np.swapaxes(test_x, 1, 3)
test_tdim, xdim, ydim, zdim = test_x.shape

#===================================================================================
# set callbacks
#===================================================================================
callbacks_list = [

  keras.callbacks.EarlyStopping(
      monitor='val_loss',
      mode='min',
      patience=100,
  ),

  keras.callbacks.ModelCheckpoint(
      filepath=main_dir+'output/cnn/model.hdf5',
      monitor='val_loss',
      save_best_only=True,
  )
]

#===================================================================================
# set model architecture
#===================================================================================
inputs = keras.Input(shape=(xdim,ydim,zdim))

conv1 = keras.layers.Conv2D(35, [3,3], activation='tanh', padding='same', strides=1)(inputs)
pool1 = keras.layers.MaxPool2D((2,2), strides=2, padding='same')(conv1)
conv2 = keras.layers.Conv2D(35, [3,3], activation='tanh', padding='same', strides=1)(pool1)
pool2 = keras.layers.MaxPool2D((2,2), strides=2, padding='same')(conv2)
conv3 = keras.layers.Conv2D(35, [3,3], activation='tanh', padding='same', strides=1)(pool2)
flat = keras.layers.Flatten()(conv3)
dense1 = keras.layers.Dense(50, activation='tanh')(flat)
outputs = keras.layers.Dense(1, activation=None)(dense1)

#===================================================================================
# run 
#===================================================================================
# compile
model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.005), 
              loss='mse')

# training
history = model.fit(tr_x, tr_y, batch_size=1024, epochs=800, verbose=1,
                    callbacks=callbacks_list,
                    validation_data=(val_x, val_y))

#===================================================================================
# save model (last epoch)
#===================================================================================
model.save(main_dir+'output/cnn/model_last.hdf5')

#===================================================================================
# save model summary and loss
#===================================================================================
# model summary
with open(main_dir+'output/cnn/model_summary.md', 'w') as f:
    with redirect_stdout(f):
        model.summary()

tr_loss = history.history['loss']
tr_loss = np.array(tr_loss)
tr_loss.astype('float32').tofile(main_dir+'output/cnn/tr_loss.gdat')

#===================================================================================
# test
#===================================================================================
# load model
model = keras.models.load_model(main_dir+'output/cnn/model.hdf5')

# prediction
fcst = model.predict(test_x)

# save
fcst = np.array(fcst)
tdim = len(fcst)
fcst.astype('float32').tofile(main_dir+'output/cnn/fcst.gdat')

f = open(main_dir+'output/cnn/fcst.ctl','w')
f.write(
'dset ^fcst.gdat\n\
undef -9.99e+08\n\
xdef   1  linear   0.  2.5\n\
ydef   1  linear -90.  2.5\n\
zdef   1  linear 1 1\n\
tdef '+str(tdim)+'  linear jan1980 1yr\n\
vars   1\n\
nino    1   1  Nino3.4\n\
ENDVARS\n'
)
f.close()

os.system('cdo -f nc import_binary '+main_dir+'output/cnn/fcst.ctl '+main_dir+'output/cnn/fcst.nc')
os.system('rm -f '+main_dir+'output/cnn/fcst.ctl '+main_dir+'output/cnn/fcst.gdat')

