#%%
import bikeprediction as bp
import pandas as pd
import numpy as np
import string
import os

import tensorflow as tf # for neural network

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

import matplotlib.pyplot as plt


#%%
# Import bikes data 
url_bike = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
target_bike = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data", "data_bike.csv")
df_bike = bp.Load_data(url_bike, target_bike).save_as_df(target_bike)


#%%

# Import weather data 

# Weather data in Montpellier in 2020 
df_weather20 = pd.read_csv("./bikeprediction/data/data_weather20.csv")

# Weather data in Montpellier in 2021 (only january and february)
df_weather21 = pd.read_csv("./bikeprediction/data/data_weather21.csv")

# Concatenate the two df in one df_weather 
df_weather = pd.concat([df_weather20, df_weather21], ignore_index=True)



#%%

# df_bike columns modification
df_bike.drop(columns = df_bike.columns[4], inplace = True)
df_bike.columns = ['Date', 'Heure', 'Grand total', 'Total jour', 'Remarque']

#%%
# dataframe descriptions
# print(df_bike.describe())
# print(df_weather.describe())

# weather dataframe modification

#%%

# modify df by changing str values in elt_col_sort from column
# col in int values in increasing order from 0.
# entry  : df = weather dataframe
#          col = column we want to change
#          elt_col_sort = list of col elements which are 
#                   sorted according to some preferences
def col_str_to_int(df, col, elt_col_sort):
    dict_temp = {}
    i = 0
    for elt in elt_col_sort: 
        dict_temp[elt] = i
        i = i + 1
    for j in range(len(df[col])):
        df[col][j] = dict_temp.get(df[col][j]) # copy pb here

#%%
print(df_weather["OPINION"].unique())

opinion_str = ["météo très défavorable", "météo défavorable", "météo correcte",
            "météo favorable", "météo idéale"]

col_str_to_int(df_weather, "OPINION", opinion_str)

# verification 
print(df_weather["OPINION"].unique())


#%%
df_bike["Date"] = pd.to_datetime(df_bike["Date"],format="%d/%m/%Y")
df_bike["Heure"] = pd.to_datetime(df_bike["Heure"]).dt.time

df_weather["DATE"] = pd.to_datetime(df_weather["DATE"])
df_weather["OPINION"] = pd.to_numeric(df_weather["OPINION"])

# %%
# df_bike.dtypes
df_weather.dtypes


# %%

# %%

df = df_bike.assign(Meteo = None)


#%%

# to put in preprocess 

for j in range(df_weather.shape[0]):
    date = df_weather["DATE"][j]
    opinion = df_weather["OPINION"][j]
    df.iloc[df.Date == date, 5] = opinion



## Tensorflow part
# %%

df.drop(columns=['Remarque'], inplace=True)

# %%
df.dropna(inplace=True)

# %%
df["Date"] = pd.to_datetime(df["Date"].astype(str)+' '+df["Heure"].astype(str),format="%Y-%m-%d %H:%M:%S")

df.drop(columns=['Heure'], inplace=True)

df["joursemaine"] = df.Date.dt.dayofweek
df["jour"] = df.Date.dt.day
df["annee"] = df.Date.dt.year
df["heure"] = df.Date.dt.hour
df["minute"] = df.Date.dt.minute

df.drop(columns=['Date'], inplace=True)
df.drop(columns=['Grand total'], inplace=True)
# %%

x_train = df.copy()
x_train = x_train.assign(previous_record=0)
x_train = x_train.assign(hour_previous_record=0)
x_train = x_train.assign(minute_previous_record=0)
for i in range(1,x_train.shape[0]):
    if(x_train.iloc[i,3]==x_train.iloc[i-1,3] and x_train.iloc[i,4]==x_train.iloc[i-1,4]):
        x_train.iloc[i,7]=x_train.iloc[i-1,0]
        x_train.iloc[i,8]=x_train.iloc[i-1,5]
        x_train.iloc[i,9]=x_train.iloc[i-1,6]


x_train.drop(columns=['Total jour'], inplace=True)
x_train["Meteo"] = x_train["Meteo"].astype(int)

y_train = df["Total jour"].copy()
#%%
normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(x_train))
print(normalizer.mean.numpy())

print('Normalized:', normalizer(x_train).numpy())
# %%
model = keras.Sequential([
      normalizer,
      layers.Dense(9, activation='relu'),
      layers.Dense(512, activation='relu'),
      layers.Dense(512, activation='relu'),
      layers.Dense(512, activation='relu'),
      layers.Dense(1)
  ])

#%%
model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

# %%
model.fit(
    x_train, y_train,
    epochs=40,
    # Calculate validation results on 20% of the training data
    validation_split = 0.2)
# %%
test=x_train.iloc[0]
print(test.shape)
model.predict(x_train)
# %%
