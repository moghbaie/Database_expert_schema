# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 01:22:09 2017

@author: moghb
"""
import numpy as np
import pandas as pd
#import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from getStringData import make_test_dataset, make_train_dataset


x_train, y_train = make_train_dataset('POM34')
x_batch1, y_batch1 = make_train_dataset('NDC80')
x_batch2, y_batch2 = make_train_dataset('NUP133')
x_batch3, y_batch3 = make_train_dataset('snRNP')
x_batch4, y_batch4 = make_train_dataset('GLC7')
x_batch5, y_batch5 = make_train_dataset('PCNA')
#x_batch6, y_batch6 = make_train_dataset('CTL1')
x_batch7, y_batch7 = make_train_dataset('SRP1')
x_batch8, y_batch8 = make_train_dataset('NIC96')
x_batch9, y_batch9 = make_train_dataset('NUP145')
x_batch10, y_batch10 = make_train_dataset('NUP1')

x_test, y_test , label_test = make_test_dataset('NUP53')

model = Sequential()
model.add(Dense(8, input_dim=8, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(8, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
"""
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
"""

model.fit(x_train, y_train,
          epochs=20,
          batch_size=128)

model.train_on_batch(x_batch1, y_batch1)
model.train_on_batch(x_batch2, y_batch2)
model.train_on_batch(x_batch3, y_batch3)
model.train_on_batch(x_batch4, y_batch4)
model.train_on_batch(x_batch5, y_batch5)
#model.train_on_batch(x_batch6, y_batch6)
model.train_on_batch(x_batch7, y_batch7)
model.train_on_batch(x_batch8, y_batch8)
model.train_on_batch(x_batch9, y_batch9)
model.train_on_batch(x_batch10, y_batch10)


score = model.evaluate(x_test, y_test, batch_size=128)
print(score)

y_pred = model.predict(x_test)
output = np.array((y_pred>.5).astype(int))
label_test
