"""
First, you need to collect training data and deploy it like this.

  ./data/
    train/
      pizza/
        pizza1.jpg
        pizza2.jpg
        ...
      poodle/
        poodle1.jpg
        poodle2.jpg
        ...
    validation/
      pizza/
        pizza1.jpg
        pizza2.jpg
        ...
      poodle/
        poodle1.jpg
        poodle2.jpg
        ...
"""

import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"        # specify gpu numbers to use
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"        # specify gpu numbers to use

import sys
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense, Activation, Reshape
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras import callbacks

print('Reading command line arguments')
DEV = False
argvs = sys.argv
argc = len(argvs)

if argc > 1 and (argvs[1] == "--development" or argvs[1] == "-d"):
  DEV = True

if DEV:
  epochs = 4
else:
  epochs = 20

print('Defining model parameters')
train_data_dir = './images/training'
validation_data_dir = './images/validation'

img_width, img_height = 150, 150
#img_width, img_height = 150, 150
#img_width, img_height = None, None
nb_train_samples = 400
nb_validation_samples = 100
nb_filters1 = 32
nb_filters2 = 64
conv1_size = 3
conv2_size = 2
pool_size = 2
classes_num = 2
batch_size = 32
lr = 0.0004

print('Defining model')
model = Sequential()
model.add(Conv2D(nb_filters1, (conv1_size, conv1_size), padding="same", input_shape=(img_width, img_height, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))

model.add(Conv2D(nb_filters2, (conv2_size, conv2_size), padding="same"))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size), data_format='channels_last'))

model.add(Flatten())
#model.add(Reshape((75*75*64, )))
model.add(Dense(256))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(classes_num, activation='softmax'))

print('Compiling model')
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=lr),
              metrics=['accuracy'])

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(
    rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

"""
Tensorboard log
"""
log_dir = './tf-log/'
tb_cb = callbacks.TensorBoard(log_dir=log_dir, histogram_freq=0)
cbks = [tb_cb]

print('Fitting model weights')
model.fit_generator(
    train_generator,
    samples_per_epoch=nb_train_samples,
    epochs=epochs,
    validation_data=validation_generator,
    callbacks=cbks,
    validation_steps=nb_validation_samples)

print('Saving model')
target_dir = './models/'
if not os.path.exists(target_dir):
  os.mkdir(target_dir)
model.save('./models/model.h5')
model.save_weights('./models/weights.h5')
