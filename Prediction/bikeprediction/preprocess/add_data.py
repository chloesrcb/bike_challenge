import pandas as pd
from pandas import Index
import numpy as np
import matplotlib.pyplot as plt
import string


def add_record(df_bike):
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
    
    return df_bike


def add_confinement(df_bike):
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
    return df_bike


def add_couvre_feu(df_bike):
    # add "couvre-feu" data (in Montpellier)
    # 17/10/20 to 28/10/20: 21h to 6h
    # 29/10/20 : de 21h to 0h00
    # 15/12/20 to 23/12/20: 20h to 6h. 
    # 25/12/20 to 15/01/21 : 20h to 6h
    # 16/01/21 to 19/03/21 : 18h to 6h
    # 20/03/21 to today : 19h to 6h
    df_bike = add_record(df_bike)
    df_bike = df_bike.assign(couvre_feu=0)
    column_index = Index(df_bike.columns)
    for i in range(df_bike.shape[0]):
        date = df_bike.iloc[i,column_index.get_loc("Date")]
        hour = df_bike.iloc[i,column_index.get_loc("heure")]
        hour_previous = df_bike.iloc[i,column_index.get_loc("hour_previous_record")]

        if date >= pd.to_datetime("2020-10-17") and date <= pd.to_datetime("2020-10-28"):
            if (hour >= 21 or hour < 6) and (hour_previous >= 21 or hour_previous < 6):
                df_bike.iloc[i,column_index.get_loc("couvre_feu")] = 1

        if date == pd.to_datetime("2020-10-29"):
            if (hour >= 21 or hour < 0) and (hour_previous >= 21 or hour_previous < 0):
                df_bike.iloc[i,column_index.get_loc("couvre_feu")] = 1

        if date >= pd.to_datetime("2020-12-15") and date <= pd.to_datetime("2020-12-24"):
            if (hour >= 20 or hour < 6) and (hour_previous >= 20 or hour_previous < 6):
                df_bike.iloc[i,column_index.get_loc("couvre_feu")] = 1

        if date >= pd.to_datetime("2020-12-25") and date <= pd.to_datetime("2021-01-15"):
            if (hour >= 20 or hour < 6) and (hour_previous >= 20 or hour_previous < 6):
                df_bike.iloc[i,column_index.get_loc("couvre_feu")] = 1

        if date >= pd.to_datetime("2021-01-16") and date <= pd.to_datetime("2021-03-19"):
            if (hour >= 18 or hour < 6) and (hour_previous >= 18 or hour_previous < 6):
                df_bike.iloc[i,column_index.get_loc("couvre_feu")] = 1

        if date > pd.to_datetime("2021-03-19"):
            if (hour >= 19 or hour < 6) and (hour_previous >= 19 or hour_previous < 6):
                df_bike.iloc[i,column_index.get_loc("couvre_feu")] = 1
    return df_bike
