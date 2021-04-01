#%%
import bikeprediction as bp
import pandas as pd
from pandas import Index
import numpy as np
import matplotlib.pyplot as plt
import string
import os

import tensorflow as tf # for neural network
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

#%%
# Import bikes data 
url_bike = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
target_bike = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bikeprediction", "data", "data_bike.csv")

df_bike_raw = bp.Load_data(url_bike, target_bike).save_as_df(target_bike)

#%%

# Import weather data 

# Weather data in Montpellier in 2020 
df_weather20 = pd.read_csv("./bikeprediction/data/data_weather20.csv")

# Weather data in Montpellier in 2021 (only january and february)
df_weather21 = pd.read_csv("./bikeprediction/data/data_weather21.csv")

# March values aren't appload yet on "Historique Météo" so I enter data manually from another website.

# Concatenate the two df in one df_weather 
df_weather = pd.concat([df_weather20, df_weather21], ignore_index=True)

#%%

# format df_weather by changing "OPINION" values and "DATE" type in datetime type
df_weather = bp.format_weather(df_weather)

#%%
# df_bike_raw columns modification
# drop an empty column
df_bike_raw.drop(columns = df_bike_raw.columns[4], inplace = True)
df_bike_raw.columns = ['Date', 'Heure', 'Grand total', 'Total jour', 'Remarque']

# remove "Remarque" column because it has only one value and it's not really usefull
df_bike_raw.drop(columns=['Remarque'], inplace=True)
df_bike_raw.dropna(inplace=True)

# %%
# format to datetime 
df_bike_raw["Date"] = pd.to_datetime(df_bike_raw["Date"],format="%d/%m/%Y")
df_bike_raw["Heure"] = pd.to_datetime(df_bike_raw["Heure"]).dt.time

# %%
# add a column "meteo" to a new dataframe df_bike, copy of df_bike_raw
df_bike = df_bike_raw.copy()
df_bike = df_bike.assign(meteo = None)
df_bike = df_bike.assign(vent = None)
df_bike = df_bike.assign(pluie = None)

#%%

# put weather opinion value in df_bike according to the date
df_bike = bp.connect_df(df_bike, df_weather, "Date", "DATE", "OPINION", 4)

#%%
df_bike = bp.connect_df(df_bike, df_weather, "Date", "DATE", "WINDSPEED_MAX_KMH", 5)

#%%

df_bike = bp.connect_df(df_bike, df_weather, "Date", "DATE", "PRECIP_TOTAL_DAY_MM", 6)


#%%
# format df_bike by changing date format in datetime, 
# removing some useless column and adding some others like day, month, year...
df_bike = bp.format_bike(df_bike)


#%%
df_bike = bp.add_confinement(df_bike)
df_bike = bp.add_couvre_feu(df_bike)

#%%
# adding holiday 
# df_bike = bp.add_holiday(df_bike)
# I remove it because it doesn't improve prediction,
# it makes it worse

#%%
df_bike.drop(columns=['Date'], inplace=True)

# TENSORFLOW PART :
# %%

# dataframe that will be processed and split for the training and the test.
x_train = df_bike.copy()

# x_train = x_train[x_train.hour_previous_record == 0]
# x_train = x_train[x_train.annee == 2021]

#%%
y_pred, test_label, model, test_dataset = bp.training(x_train)

#%%
x = tf.linspace(0, test_label.shape[0]-1, test_label.shape[0])

#%%
# plot prediction
fig = plt.figure(figsize=(8,4))
bp.plot_prediction(x,y_pred, test_label)
fig.savefig('prediction.pdf')

# %%
#model.predict(pd.DataFrame(test_dataset.iloc[0]).T)



# Testing model prediction :

# %%
decembre22 = bp.prediction(model, weather=2, wind=8, rain=0, weekday=1, day=22, month=12, year=2020, hour=12, minute=34, workingday=1, confinement=0, previous_record=231, hour_previous_record=11, minute_previous_record=51, couvre_feu=0)
# find 263 and the real record was 268 at 12:34

#%%
march27 = bp.prediction(model, weather=2, wind=24, rain=0, weekday=5, day=27, month=3, year=2021, hour=9, minute=27, workingday=0, confinement=0, previous_record=52, hour_previous_record=8, minute_previous_record=29, couvre_feu=0)
# find 127 and the real record was 111 at 9:27

#%%
april1 = bp.prediction(model, weather=2, wind=6, rain=0, weekday=3, day=1, month=4, year=2021, hour=9, minute=37, workingday=1, confinement=0, previous_record=0, hour_previous_record=0, minute_previous_record=0, couvre_feu=0)
# find 426 and the real record was 437 at 9:37

# Prediction on 2nd April at 9:00 :
# %%
april2 = bp.prediction(model, weather=2, wind=19, rain=0, weekday=4, day=2, month=4, year=2021, hour=9, minute=0, workingday=1, confinement=0, previous_record=0, hour_previous_record=0, minute_previous_record=0, couvre_feu=0)
print(april2)
# find 335

# %%
