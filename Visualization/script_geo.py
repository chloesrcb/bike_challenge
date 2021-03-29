#%%
import bikevisualization as bv
import pandas as pd
import numpy as np
import string, os
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
import folium
import branca.colormap as cm
import requests, tempfile, zipfile
from shapely.geometry import shape
#%%

montpellier = gpd.read_file("./bikevisualization/data/montpellier.json")
montpellier.head()

#%%

ax = montpellier.plot(figsize=(10,10), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax, crs = montpellier.crs.to_string())
ax
plt.show()
#%%

df_counters = bv.Load_json().save_as_df()
# format data for all dataframe in df_counters
df_counters = bv.format_dfs(df_counters)
#%%
df_berracasa = df_counters[0]

# %%
# Changing dataFrame format to GeodataFrame
gdf_counters=[]
for i in range(len(df_counters)):
    df_counters[i]['location'] = df_counters[i]['location'].apply(shape)
    gdf_counters.append(gpd.GeoDataFrame(df_counters[i]))
    gdf_counters[i]["geometry"]=gdf_counters[i]['location']

#%%
# Creating Date List

dates = []
for i in range(len(df_counters)):
    dates = list(set(dates) | set(df_counters[i].index))
dates.sort()


#%%
numFile=0
#'2021-03-28' in gdf_counters[0].index
for date in dates:
    print(date)
    ax = montpellier.plot(figsize = (10, 10), zorder=1, edgecolor='black', facecolor='none', color=None)
    for i in range(len(df_counters)):
        if(date in gdf_counters[i].index and len(gdf_counters[i].loc[date].shape)==1):
            current_loc = gpd.GeoDataFrame(gdf_counters[i].loc[date].to_frame().T)
            current_loc.plot(ax = ax, color = 'red', alpha = 0.8, zorder = 2, markersize=current_loc["intensity"][date])

    ctx.add_basemap(ax, crs=montpellier.crs.to_string(), source=ctx.providers.Stamen.Watercolor)
    ax.set_axis_off()
    plt.title(f"Intensities of bikes at the date {date.year}-{date.month}-{date.day}")
    plt.tight_layout(pad=0)
    #plt.show()
    plt.savefig(f"bikevisualization/images/{numFile}.jpg")
    numFile+=1
# %%

# %%
