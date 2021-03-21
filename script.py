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


#%%

# put weather opinion value in df_bike according to the date
df_bike = bp.connect_df(df_bike, df_weather, "Date", "DATE", "OPINION")

#%%

# format df_bike by changing date format in datetime, 
# removing some useless column and adding some others like day, month, year...
df_bike = bp.format_bike(df_bike)

#%%

# TODO : WINDSPEED to add ?

#%%

# add "confinement" data (in France)
# from 03/17/2020 at 12 h to 05/11/2020 (not include) 
# from 10/30/2020 to 12/15/2020 (not include)
df_bike = df_bike.assign(confinement=0)
column_index = Index(df_bike.columns)
for i in range(df_bike.shape[0]):
    date = df_bike.iloc[i,column_index.get_loc("Date")]
    if date >= pd.to_datetime("2020-03-17 12:00:00") and date <= pd.to_datetime("2020-05-11 00:00:00"):
        df_bike.iloc[i,column_index.get_loc("confinement")] = 1
    if  date >= pd.to_datetime("2020-10-30 00:00:00") and date <= pd.to_datetime("2020-12-15 00:00:00"):
        df_bike.iloc[i,column_index.get_loc("confinement")] = 1


#%%
df_bike = df_bike.assign(previous_record=0)
df_bike = df_bike.assign(hour_previous_record=0)
df_bike = df_bike.assign(minute_previous_record=0)

# TODO : ajouter un previous record en temps écoulé pour voir si c'est mieux

column_index = Index(df_bike.columns)
for i in range(1, df_bike.shape[0]):
    if(df_bike.iloc[i, column_index.get_loc("jour")] == df_bike.iloc[i-1, column_index.get_loc("jour")] and df_bike.iloc[i, column_index.get_loc("annee")] == df_bike.iloc[i-1, column_index.get_loc("annee")]):
        df_bike.iloc[i, column_index.get_loc("previous_record")] = df_bike.iloc[i-1, column_index.get_loc("Total jour")]
        df_bike.iloc[i, column_index.get_loc("hour_previous_record")] = df_bike.iloc[i-1, column_index.get_loc("heure")]
        df_bike.iloc[i, column_index.get_loc("minute_previous_record")] = df_bike.iloc[i-1, column_index.get_loc("minute")]


#%%

# add "couvre-feu" data (in Montpellier)
#     : 20h
# 16 janvier 2021 jusqu'au 19/03/21 : 18h à 6h
# 20/03/21 à ....  : 19h à (7h ?)
# 17/10/20 minuit jusqu'au 30/10/20 minuit : de 21h à 6h
#  à 12 h au 11 mai 2020 (non inclus), 
# du 30 octobre 2020 au 15 décembre 2020 (non inclus)
df_bike = df_bike.assign(couvre_feu=0)
column_index = Index(df_bike.columns)
for i in range(df_bike.shape[0]):
    date = df_bike.iloc[i,column_index.get_loc("Date")]
    hour = df_bike.iloc[i,column_index.get_loc("heure")]
    hour_previous = df_bike.iloc[i,column_index.get_loc("hour_previous_record")]


    if date >= pd.to_datetime("2021-01-16") and date <= pd.to_datetime("2021-03-19"):
        if (hour >= 18 or hour < 6) and (hour_previous >= 18 or hour_previous < 6):
            df_bike.iloc[i,column_index.get_loc("couvre_feu")] = 1

    # if  df_bike.loc[i,"Date"] >= pd.to_datetime("2021-03-20"):
    #     if df_bike.loc[i,"heure"] >= 19 and df_bike.loc[i,"heure"] < 7:
    #         df_bike.loc[i,"couvre_feu"] = 1
    # if  df_bike.loc[i,"Date"] >= pd.to_datetime("2021-03-20"):
    #     if df_bike.loc[i,"heure"] >= 19 and df_bike.loc[i,"heure"] < 7:
    #        df_bike.loc[i,"couvre_feu"] = 1

# TODO: Finir les dates du couvre feu, attention pose probleme selon heure de relevé le soir...


#%%
df_bike.drop(columns=['Date'], inplace=True)

# TENSORFLOW PART :
# %%

x_train = df_bike.copy()

# x_train = x_train[x_train.hour_previous_record == 0]

# x_train = x_train[x_train.annee == 2021]

#%%
x_train.dropna(inplace=True)
x_train["meteo"] = x_train["meteo"].astype(int)

train_dataset = x_train.sample(frac=0.8, random_state=0).copy()
train_label = train_dataset.pop("Total jour")

test_dataset = x_train.drop(train_dataset.index)
test_label = test_dataset.pop("Total jour")

#%%
normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(train_dataset))
print(normalizer.mean.numpy())

print('Normalized:', normalizer(train_dataset).numpy())

tf.random.set_seed(0)

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

fig = plt.figure(figsize=(8,4))
plot_prediction(x,y_pred, test_label)
fig.savefig('prediction.pdf')  # sauvegarde dans le disk sous le nom de toto.pdf 

# %%
model.predict(pd.DataFrame(test_dataset.iloc[0]).T)
# %%

# Prediction for 04/02/2021
avril2 = pd.DataFrame(test_dataset.iloc[0]).T
avril2["joursemaine"] = 4.0
avril2["jour"] = 2.0
avril2["mois"] = 4.0
avril2["annee"] = 2021.0
avril2["heure"] = 9.0
avril2["travail"] = 1.0
avril2["confinement"] = 0.0
avril2["couvre_feu"] = 0.0
model.predict(avril2)


# %%
