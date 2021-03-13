import bikeprediction as bp



# import data 
df_bike = bp.Load_data().save_as_df()

# columns names modification
df_bike.columns = ['Date', 'Heure', 'Grand total', 'Total jour', 'None', 'Remarque']

# dataframe description
print(df_bike.describe())