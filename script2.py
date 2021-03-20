
#%%
import bikeprediction as bp
import pandas as pd
import numpy as np
import string
import os
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
import folium
import branca.colormap as cm

# #%%
# url_traffic = "https://data.montpellier3m.fr/node/12001/download"
# target_traffic = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data", "data_traffic.csv")
# df_traffic = bp.Load_data(url_traffic, target_traffic).save_as_df(target_traffic)

# %%

import string
import requests
import tempfile
import zipfile


# data containing geometric data on French cities
# url = 'https://www.data.gouv.fr/fr/datasets/r/07b7c9a2-d1e2-4da6-9f20-01a7b72d4b12'
# temporary_location = tempfile.gettempdir() 

# # unzip file or folder from an url
# # to put in covidmap ??
# def download_unzip(url, dirname, destname):
#   myfile = requests.get(url)
#   open(dirname + '/' + destname + '.zip', 'wb').write(myfile.content)
#   with zipfile.ZipFile(dirname + '/' + destname + '.zip', 'r') as zip_ref:
#     zip_ref.extractall(dirname + '/' + destname)


# download_unzip(url, temporary_location, "borders")

# # dataframe of the cities in France
# cities = gpd.read_file(temporary_location + "/borders/communes-20190101.json")


montpellier_geo = gpd.read_file("./bikeprediction/data/montpellier.json")
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
%matplotlib inline

# #%%

# dates = [i['timestamp'] for i in data["data"]]
# values = [i['bytes'] for i in data['data']]

# df = pd.DataFrame({'dates':dates, 'values':values})
# df['dates']  = [pd.to_datetime(i) for i in df['dates']]

# print(df.sort_values(by='dates'))

#                 dates  values
# 1 2018-01-21 22:33:14   37892
# 0 2018-01-21 22:34:34   29466
# 2 2018-01-21 22:37:40   36396

# plt.bar(dates, values)


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


# %%
