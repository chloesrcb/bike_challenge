import numpy as np
import pandas as pd
import tensorflow as tf # for neural network
from tensorflow import keras


def prediction(model, weather=0, wind=0, rain=0, weekday=0, day=0, month=0, year=0, hour=0, minute=0, workingday=0, confinement=0,previous_record=0, hour_previous_record=0, minute_previous_record=0, couvre_feu=0):
    """
        Return the prediction for a specific day and a specific hour
        entry : model = prediction model
                weather = opinion weather for the day, int in {0,...,4}
                wind = wind speed max for the day, int
                rain = rain precipitation for the day, float
                weekday = which week day is it from 0 (Monday) to 6 (Sunday)
                day = day number of the day wanted, int in {1,...,31} according to the month
                month = month of the day wanted, int in {1,...,12}
                year = date year for the day, int
                hour = hour wanted 
                minute = minute wanted
                workingday = if the day is a working day or not (0 or 1)
                confinement = if the day is lockdown day or not (0 or 1)
                previous_record = last value recorded of the day before the date and hour wanted,
                        0 if there was no previous record in the day
                hour_previous_record = hour of the last record
                minute_previous_record = minute of the last record
                couvre_feu = if date + hour is during a curphew (0 or 1)
    """
    predict_day_tab = {
                   "meteo" : [float(weather)],
                   "vent" : [int(wind)],
                   "pluie" : [float(rain)],
                   "joursemaine" : [float(weekday)],
                   "jour" : [float(day)],
                   "mois" : [float(month)],
                   "annee" : [float(year)],
                   "heure" : [float(hour)],
                   "minute" : [float(minute)],
                   "travail" :[float(workingday)],
                   "confinement": [float(confinement)],
                   "previous_record" : [float(previous_record)],
                   "hour_previous_record" : [float(hour_previous_record)],
                   "minute_previous_record" : [float(minute_previous_record)],
                   "couvre_feu": [float(couvre_feu)]}
    
    predict_day_df = pd.DataFrame(data = predict_day_tab)

    res = model.predict(predict_day_df)
    return res