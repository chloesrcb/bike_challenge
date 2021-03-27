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

#%%
df_berracasa = df_counters[0]

#%%

df_berracasa['location'] = df_berracasa['location'].apply(shape)
loc = gpd.GeoDataFrame(df_berracasa)
loc["geometry"]=loc['location']
current_loc = gpd.GeoDataFrame(loc.iloc[0].to_frame().T)

ax= current_loc.plot(figsize = (15, 15), color = 'red', alpha = 0.8, zorder = 2)
montpellier.plot(ax = ax, zorder=1, edgecolor='black', facecolor='none', color=None)
ctx.add_basemap(ax, crs=montpellier.crs.to_string(), source=ctx.providers.Stamen.Watercolor)
ax.set_axis_off()
plt.tight_layout(pad=0)
plt.show()
# %%

df_berracasa['location'] = df_berracasa['location'].apply(shape)
loc = gpd.GeoDataFrame(df_berracasa)
loc["geometry"]=loc['location']
current_loc = gpd.GeoDataFrame(loc.iloc[0].to_frame().T)


ax = montpellier.plot(figsize = (10, 10), zorder=1, edgecolor='black', facecolor='none', color=None)
current_loc.plot(ax = ax, color = 'red', alpha = 0.8, zorder = 2, markersize=current_loc["intensity"][0])
ctx.add_basemap(ax, crs=montpellier.crs.to_string(), source=ctx.providers.Stamen.Watercolor)
ax.set_axis_off()
plt.tight_layout(pad=0)
plt.show()

df_berracasa['location'] = df_berracasa['location'].apply(shape)
loc = gpd.GeoDataFrame(df_berracasa)
loc["geometry"]=loc['location']
current_loc = gpd.GeoDataFrame(loc.iloc[1].to_frame().T)

# %%
