#%%

import bikeprediction as bp
import pandas as pd
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
target_bike = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data", "data_bike.csv")
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

# %%
# format to datetime 
df_bike_raw["Date"] = pd.to_datetime(df_bike_raw["Date"],format="%d/%m/%Y")
df_bike_raw["Heure"] = pd.to_datetime(df_bike_raw["Heure"]).dt.time


#%%
# dataframe descriptions
# print(df_bike_raw.describe())
# print(df_weather.describe())


# %%

# add a column "meteo" to a new dataframe df_bike, copy of df_bike_raw
df_bike = df_bike_raw.copy()
df_bike = df_bike.assign(meteo = None)


#%%

# put weather opinion value in df_bike according to the date
df_bike = bp.connect_df(df_bike, df_weather, "Date", "DATE", "OPINION")

#%%

# format df_bike by changing date format in datetime, 
# removing some useless column and adding some others like day, month, year...
df_bike = bp.format_bike(df_bike)




# TENSORFLOW PART :
# %%

x_train = df_bike.copy()
x_train = x_train.assign(previous_record=0)
x_train = x_train.assign(hour_previous_record=0)
x_train = x_train.assign(minute_previous_record=0)
for i in range(1, x_train.shape[0]):
    if(x_train.iloc[i, 3] == x_train.iloc[i-1, 3] and x_train.iloc[i, 4] == x_train.iloc[i-1, 4]):
        x_train.iloc[i, 7] = x_train.iloc[i-1, 0]
        x_train.iloc[i, 8] = x_train.iloc[i-1, 5]
        x_train.iloc[i, 9] = x_train.iloc[i-1, 6]

#x_train=x_train[x_train.hour_previous_record == 0]

#x_train = x_train[x_train.annee == 2021]

#%%

x_train["Meteo"] = x_train["Meteo"].astype(int)

train_dataset = x_train.sample(frac=0.8, random_state=0).copy()
train_label = train_dataset.pop("Total jour")

test_dataset = x_train.drop(train_dataset.index)
test_label = test_dataset.pop("Total jour")

#%%

#%%
normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(train_dataset))
print(normalizer.mean.numpy())

print('Normalized:', normalizer(train_dataset).numpy())
# %%
model = keras.Sequential([
      normalizer,
      layers.Dense(9, activation='relu'),
      layers.Dense(64, activation='relu'),
      layers.Dense(64, activation='relu'),
      layers.Dense(1)
  ])

#%%
model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

# %%
model.fit(
    train_dataset, train_label,
    epochs=100,
    # Calculate validation results on 20% of the training data
    validation_split = 0.2)

#%% 
def plot_prediction(x, y, reference):
    plt.scatter(x, reference, label='Data')
    plt.plot(x, y, color='k', label='Predictions')
    plt.xlabel('test')
    plt.ylabel('nb velo')
    plt.legend()

# %%
y_pred = model.predict(test_dataset)
x = tf.linspace(0, test_label.shape[0]-1, test_label.shape[0])

plot_prediction(x,y_pred,test_label)
# %%

# %%
