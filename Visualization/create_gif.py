#%%
import bikevisualization as bv
import geopandas as gpd

#%%

# import montpellier map
montpellier = gpd.read_file("./bikevisualization/data/montpellier.json")
montpellier.head()

#%%

# import counters data in a list of dataframe 
df_counters = bv.Load_json().save_as_df()

#%%

# format data for all dataframe in df_counters
df_counters = bv.format_dfs(df_counters)

#%%

bv.images_gif(montpellier, df_counters)
# %%

# the gif will be generate with : 