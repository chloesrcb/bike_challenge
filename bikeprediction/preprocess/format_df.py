import pandas as pd

# modify df by changing str values in elt_col_sort from column
# col in int values in increasing order from 0.
# entry  : df = weather dataframe
#          col = column we want to change
#          elt_col_sort = list of col elements which are 
#                   sorted according to some preferences
def format_to_int(df, col, elt_col_sort):
    dict_temp = {}
    i = 0
    for elt in elt_col_sort: 
        dict_temp[elt] = i
        i = i + 1
    df[col] = df[col].map(dict_temp)
    return df


# format df_bike
# by removing useless column and NaN values
# by adding cropped date with day, mont, year, hour, minute

def format_bike(df_bike):
    # remove "Remarque" column because it has only one value and it's not really usefull
    df_bike.drop(columns=['Remarque'], inplace=True)
    df_bike.dropna(inplace=True)
    df_bike["Date"] = pd.to_datetime(df_bike["Date"].astype(str)+' '+df_bike["Heure"].astype(str),format="%Y-%m-%d %H:%M:%S")
    df_bike.drop(columns=['Heure'], inplace=True)
    # get value in new columns 
    df_bike["joursemaine"] = df_bike.Date.dt.dayofweek
    df_bike["jour"] = df_bike.Date.dt.day
    df_bike["mois"] = df_bike.Date.dt.month
    df_bike["annee"] = df_bike.Date.dt.year
    df_bike["heure"] = df_bike.Date.dt.hour
    df_bike["minute"] = df_bike.Date.dt.minute
    df_bike.drop(columns=['Date'], inplace=True)
    df_bike.drop(columns=['Grand total'], inplace=True)
    return df_bike

# format df_weather
# by changing "OPINION" column with int values from 0 to 4 like this :
#           "météo très défavorable" -> 0
#           "météo défavorable" -> 1
#           "météo correcte" -> 2
#           "météo favorable" -> 3
#           "météo idéale" -> 4
# by changing the date in datetime type
def format_weather(df_weather) :
    opinion_str = ["météo très défavorable", "météo défavorable", "météo correcte",
            "météo favorable", "météo idéale"]
    format_to_int(df_weather, "OPINION", opinion_str)
    df_weather["DATE"] = pd.to_datetime(df_weather["DATE"])
    df_weather["OPINION"] = pd.to_numeric(df_weather["OPINION"])
    return df_weather
