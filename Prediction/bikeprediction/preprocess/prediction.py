import numpy as np
import pandas as pd
import tensorflow as tf # for neural network
from tensorflow import keras


def prediction(model, test_dataset, weekday, day, month, year, hour, workingday, confinement, couvre_feu):
    predict_day = pd.DataFrame(test_dataset.iloc[0]).T
    predict_day["joursemaine"] = float(weekday)
    predict_day["jour"] = float(day)
    predict_day["mois"] = float(month)
    predict_day["annee"] = float(year)
    predict_day["heure"] = float(hour)
    predict_day["travail"] = float(workingday)
    predict_day["confinement"] = float(confinement)
    predict_day["couvre_feu"] = float(couvre_feu)
    res = model.predict(predict_day)
    return res