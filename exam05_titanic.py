#!/usr/bin/env python
# coding: utf-8

# In[1]:


import seaborn as sns
import pandas as pd
import numpy as np


# In[2]:


raw_data = sns.load_dataset('titanic')
raw_data.head(10)


# In[3]:


raw_data.info()


# In[4]:


raw_data.isnull().sum()


# In[5]:


clean_data = raw_data.dropna(axis=1, thresh=500)


# In[6]:


clean_data.columns


# In[7]:


mean_age = clean_data['age'].mean()
print(mean_age)


# In[8]:


clean_data['age'].fillna(mean_age, inplace=True)
clean_data.head(10)


# In[9]:


clean_data.drop(['embark_town', 'alive'], axis=1, inplace=True)


# In[10]:


clean_data.info()


# In[11]:


clean_data['embarked'][825:830]


# In[12]:


clean_data['embarked'].fillna(method='ffill', inplace=True)
clean_data['embarked'][825:830]


# In[14]:


clean_data.isnull().sum()


# In[15]:


clean_data.info()


# In[16]:


clean_data['sex'].replace({'male':0, 'female':1}, inplace=True)
clean_data.info()


# In[18]:


print(clean_data['sex'].unique())


# In[20]:


print(clean_data['embarked'].unique())


# In[21]:


from sklearn import preprocessing


# In[22]:


label_encoder = preprocessing.LabelEncoder()
onehot_encoder = preprocessing.OneHotEncoder()


# In[23]:


print(clean_data['embarked'].value_counts())


# In[25]:


clean_data['embarked'] = label_encoder.fit_transform(
    clean_data['embarked'])
print(clean_data['embarked'].unique())


# In[26]:


print(clean_data['embarked'].value_counts())


# In[27]:


clean_data.info()


# In[28]:


clean_data['adult_male'] = clean_data['adult_male'].astype('int64')
clean_data.info()


# In[29]:


clean_data.head()


# In[30]:


target = clean_data[['survived']]
target


# In[31]:


training_data = clean_data.drop('survived', axis=1, inplace=False)
training_data.head()


# In[32]:


value_data = training_data[['age', 'fare']]
value_data


# In[33]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(value_data)
value_data = pd.DataFrame(scaled_data, columns=value_data.columns)
value_data.head()


# In[34]:


training_data.drop(['age', 'fare'], axis=1, inplace=True)
training_data.head()


# In[35]:


onehot_data = pd.get_dummies(training_data['pclass'])
onehot_data.head()


# In[36]:


onehot_data = pd.get_dummies(training_data, columns=training_data.columns)
onehot_data.head()


# In[37]:


onehot_data.info()


# In[38]:


training_data = pd.concat([value_data, onehot_data], axis=1)
training_data.info()


# In[49]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    training_data.astype('float64'), target, test_size=0.20)


# In[50]:


print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)


# In[51]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


# In[64]:


model = Sequential()
model.add(Dense(128, input_dim=34, activation='relu'))
model.add(Dropout(0.02))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.summary()


# In[65]:


model.compile(loss='mse', optimizer='adam', metrics=['binary_accuracy'])


# In[66]:


fit_hist = model.fit(
    x_train, y_train, batch_size=50, epochs=5,
    validation_split=0.2, verbose=1)


# In[67]:


import matplotlib.pyplot as plt
plt.plot(fit_hist.history['binary_accuracy'])
plt.plot(fit_hist.history['val_binary_accuracy'])  
plt.show()


# In[68]:


score = model.evaluate(x_test, y_test, verbose=0)
print('loss', score[0])
print('accuracy', score[1])


# In[ ]:




