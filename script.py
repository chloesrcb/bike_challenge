#%%
import bikeprediction as bp
import pandas as pd
import numpy as np
import string
import os
import tensorflow as tf # for neural network
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

# Weather data in Montpellier in 2021 (only january)
df_weather21 = pd.read_csv("./bikeprediction/data/data_weather21.csv")


#%%

# df_bike columns modification
df_bike.drop(columns = df_bike.columns[4], inplace = True)
df_bike.columns = ['Date', 'Heure', 'Grand total', 'Total jour', 'Remarque']

#%%
# dataframe descriptions
# print(df_bike.describe())
# print(df_weather20.describe())
# print(df_weather21.describe())


#%%
print(df_weather20["OPINION"].unique())

# weather dataframes modification

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
opinion_str = ["météo très défavorable", "météo défavorable", "météo correcte",
            "météo favorable", "météo idéale"]

opinion_to_int(df_weather20, "OPINION", opinion_str)
opinion_to_int(df_weather21, "OPINION", opinion_str)

# verification 
print(df_weather20["OPINION"].unique())
print(df_weather21["OPINION"].unique())

#%%
df_bike["Date"] = pd.to_datetime(df_bike["Date"])
df_bike["Heure"] = pd.to_datetime(df_bike["Heure"]).dt.time
df_weather20["DATE"] = pd.to_datetime(df_weather20["DATE"])
df_weather21["DATE"] = pd.to_datetime(df_weather21["DATE"])
df_weather20["OPINION"] = pd.to_numeric(df_weather20["OPINION"])
df_weather21["OPINION"] = pd.to_numeric(df_weather21["OPINION"])

# %%
# df_bike.dtypes
df_weather21.dtypes


# %%

# %%
