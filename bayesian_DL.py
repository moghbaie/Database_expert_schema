# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 01:22:09 2017

@author: moghb
"""
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

# Generate dummy data
import numpy as np
x_train = np.random.random((1000, 8))
y_train = keras.utils.to_categorical(np.random.randint(1, size=(1000, 1)), num_classes=10)
x_test = np.random.random((100, 8))
y_test = keras.utils.to_categorical(np.random.randint(1, size=(100, 1)), num_classes=10)

model = Sequential()
model.add(Dense(64, activation='relu', input_dim=20, init="glorot_uniform"))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu', init="glorot_uniform"))
model.add(Dropout(0.5))
model.add(Dense(1, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(x_train, y_train,
          epochs=20,
          batch_size=128)

#model.train_on_batch(X_batch, Y_batch)

score = model.evaluate(x_test, y_test, batch_size=128)
