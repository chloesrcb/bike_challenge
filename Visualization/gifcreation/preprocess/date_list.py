
import pandas as pd

def date_list(df_list):
    """
        create a list of dates from df_list
    """
    dates = []
    for i in range(len(df_list)):
        dates = list(set(dates) | set(df_list[i].index))
    dates.sort()
    return dates