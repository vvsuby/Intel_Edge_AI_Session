# -*- coding: utf-8 -*-
"""exam04_heart_disease_predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HPkFymWhrdaTq9blN67C5pxIJ1Wpc4Y1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

column_name = ['age', 'sex', 'cp', 'treshbps', 'chol', 'fbs', 'restecg',
               'thalach', 'exang', 'oldpeak', 'slop', 'ca', 'thal',
               'HeartDisease']
raw_data = pd.read_excel('./datasets/heart-disease.xlsx',
                         header=None, names=column_name)
print(raw_data.head())

raw_data.info()

raw_data.describe()

clean_data = raw_data.replace('?', np.nan)
clean_data = clean_data.dropna()
clean_data.info()

keep = column_name.pop()
print(keep)
print(column_name)

training_data = clean_data[column_name]
target = clean_data[[keep]]
print(training_data)
print(target)

print(target['HeartDisease'].sum())

print(target['HeartDisease'].mean())

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(training_data)
scaled_data = pd.DataFrame(scaled_data, columns=column_name)
print(scaled_data)

scaled_data.describe()

scaled_data.describe().T

boxplot = scaled_data.boxplot(column=column_name, showmeans=True)
plt.show()

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    scaled_data, target, test_size=0.30)
print('x_train shape', x_train.shape)
print('y_train shape', y_train.shape)
print('x_test shape', x_test.shape)
print('y_test shape', y_test.shape)

model = Sequential()
model.add(Dense(512, input_dim=13, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(1, activation='sigmoid'))
model.summary()

model.compile(loss='mse', optimizer='adam', metrics=['binary_accuracy'])
fit_hist = model.fit(x_train, y_train, batch_size=50, epochs=20,
                     validation_split=0.2, verbose=1)

plt.plot(fit_hist.history['binary_accuracy'])
plt.plot(fit_hist.history['val_binary_accuracy'])
plt.show()

score = model.evaluate(x_test, y_test, verbose=0)
print('Keras DNN model loss :', score[0])
print('Keras DNN model accuracy :', score[1])

