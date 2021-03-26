#%%
import bikevisualization as bv
import pandas as pd
import numpy as np
import string
import os
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
import folium
import branca.colormap as cm
import string
import requests
import tempfile
import zipfile

#%% 
montpellier_geo = gpd.read_file("./bikevisualization/data/montpellier.json")
montpellier_geo.head()

#%%
ax = montpellier_geo.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax, crs = montpellier_geo.crs.to_string())
ax
# plt.tight_layout(pad=0)
plt.show()


#%%
df = pd.read_csv("./bikeprediction/data/visu.json")
ax = df.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
ax

# %%
import json
import pandas as pd
import matplotlib.pyplot as plt

#%%
data = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042633.json"

bla = gpd.read_file(data)


ax = bla.plot(figsize = (10,10), color = 'red', alpha = 0.8, zorder=2)
montpellier_geo.plot(ax = ax, zorder=1, edgecolor = "black", facecolor="none", color = None)
ctx.add_basemap(ax, crs = bla.crs.to_string(), source = ctx.providers.Stamen.Watercolor)
ax.set_axis_off()
plt.tight_layout(pad=0)
plt.show()



# %%
import urllib, json

#%%
url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042633_archive.json"

response = urllib.request.urlopen(url)
webContent = response.read()

str_content=str(webContent)
str_content="["+str_content[5:-1]+"]"
str_content=str_content.replace("\\n","")
str_content=str_content.replace("} {","},{")
str_content=str_content.replace("}  {","},{")
str_content=str_content.replace("}{","},{")

data = pd.read_json(str_content)
#%%
#print(data)

from shapely.geometry import shape

data['location'] = data['location'].apply(shape)

loc=gpd.GeoDataFrame(data)

#loc.geometry=loc.location.copy()

current_loc = gpd.GeoDataFrame(loc.iloc[0].to_frame().T)
#current_loc.iloc[3] = current_loc.iloc[3].apply(shape)
#current_loc.set_geometry(current_loc.iloc[3])

ax = current_loc.plot(figsize = (current_loc.intensity,current_loc.intensity), color = 'red', alpha = 0.8, zorder=2)
montpellier_geo.plot(ax = ax, zorder=1, edgecolor = "black", facecolor="none", color = None)
ctx.add_basemap(ax, crs = bla.crs.to_string(), source = ctx.providers.Stamen.Watercolor)
ax.set_axis_off()
plt.tight_layout(pad=0)
plt.show()


