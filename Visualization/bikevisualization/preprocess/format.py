import pandas as pd

# for all df in df_list, add a column date and a column weekday
# and put date in index

def format_dfs(df_list):
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
