import bikeprediction as bp
import pandas as pd
import numpy as np
import string
import os


# import data on bikes 
url_bike = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
target_bike = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data", "data_bike.csv")
df_bike = bp.Load_data(url_bike, target_bike).save_as_df(target_bike)

# Import weather data 

# Weather data in Montpellier in 2020 
df_weather20 = pd.read_csv("./bikeprediction/data/data_weather20.csv")

# Weather data in Montpellier in 2021 (only january)
df_weather21 = pd.read_csv("./bikeprediction/data/data_weather21.csv")

# columns modification
df_bike.drop(columns = df_bike.columns[4], inplace = True)
df_bike.columns = ['Date', 'Heure', 'Grand total', 'Total jour', 'Remarque']

# dataframe descriptions
#print(df_bike.describe())
#print(df_weather20.describe())
#print(df_weather21.describe())

print(df_weather20["OPINION"].unique())

# weather dataframes modification
# In column "OPINION" :
#       'météo très défavorable' -> 0
#       'météo défavorable' -> 1
#       'météo correcte' -> 2
#       'météo favorable' -> 3
#       'météo idéale' -> 4

def opinion_to_int(df, col="OPINION"):
    dic_temp = {"météo très défavorable": 0,
                "météo défavorable": 1,
                "météo correcte": 2,
                "météo favorable": 3,
                "météo idéale": 4}
    for i in range(len(df[col])):
        df[col][i]=dic_temp.get(df[col][i])

opinion_to_int(df_weather20)
print(df_weather20["OPINION"].unique())
