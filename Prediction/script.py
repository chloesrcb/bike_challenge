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

x_train = df_bike.copy()

# x_train = x_train[x_train.hour_previous_record == 0]
# x_train = x_train[x_train.annee == 2021]

#%%
y_pred, x, test_label, model, test_dataset = bp.training(x_train)

#%%
fig = plt.figure(figsize=(8,4))
bp.plot_prediction(x,y_pred, test_label)
fig.savefig('prediction.pdf')

# %%
#model.predict(pd.DataFrame(test_dataset.iloc[0]).T)

# %%
april2 = bp.prediction(model, test_dataset, 4, 2, 4, 2021, 9, 1, 0, 0)

#%%
march27 = bp.prediction(model, test_dataset, 5, 27, 3, 2021, 9, 0, 0, 0)

# Prediction = 134 (à vérifier) avant changement archi
# = 169 apres changement (peut etre à cause de la seed  ???)


# %%
