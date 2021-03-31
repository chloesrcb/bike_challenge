import numpy as np
import pandas as pd
import tensorflow as tf # for neural network
from tensorflow import keras


def prediction(model, weather=0, wind=0, rain=0, weekday=0, day=0, month=0, year=0, hour=0, minute=0, workingday=0, confinement=0,previous_record=0, hour_previous_record=0, minute_previous_record=0, couvre_feu=0):
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