import pandas as pd

def format_dfs(df_list):
    """
        For all df in df_list, add a column date and a column weekday
        and put date in index
        The column date corresponding to the first date in the first part of "dateObserved" in dfs
        The column weekday corresponding to day of week : 0 for Monday to 6 for Sunday
        Entry : df_list = list of dataframes
        Return : df_list modified with new columns "date" and "weekday" and "dateObserved" removed
    """
    for i in range(10) :
        df_list[i] = df_list[i].assign(date=0)
        df_list[i] = df_list[i].assign(weekday=0)
        column_index = df_list[i].columns
        for j in df_list[i].index :
            date = df_list[i].iloc[j,column_index.get_loc("dateObserved")][0:10]
            df_list[i].iloc[j, column_index.get_loc("date")] = pd.to_datetime(date, format="%Y-%m-%d")
        df_list[i].date = pd.to_datetime(df_list[i].date)
        df_list[i].weekday = df_list[i].date.dt.dayofweek
        df_list[i] = df_list[i].set_index(["date"])
        df_list[i] = df_list[i].sort_index()
        df_list[i].drop(columns="dateObserved")
    return df_list
