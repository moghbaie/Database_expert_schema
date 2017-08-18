# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 22:46:32 2017

@author: moghb
"""

from getStringData import make_test_dataset, make_train_dataset
from sklearn.naive_bayes import GaussianNB

clf = GaussianNB()
x_train, y_train = make_train_dataset('POM34')
x_test, y_test , label_test = make_test_dataset('NUP53')

clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)
print(clf.predict(x_test))

