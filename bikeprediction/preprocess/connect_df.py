

# add values from a dataframe to another according to a colunm they 
# have in common
# df : dataframe you want to change
# df_val : dataframe where are values wanted
# col : column from df in common with df_val
# col_same : column from df in common with df 
# col_val : column where are the values wanted

def connect_df(df, df_val, col, col_same, col_val):
    for j in range(df_val.shape[0]):
        temp = df_val[col_same][j]
        value = df_val[col_val][j]
        df.iloc[df[col] == temp, 4] = value
    return df