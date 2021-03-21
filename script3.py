
# %%
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
import urllib, json

%matplotlib inline
#%%

df_counters = bv.Load_json().save_as_df()



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

# %%
# import calendar
# df_bikes['month'] = df_bikes.index.month  # Janvier=0, .... Decembre=11
# df_bikes['month'] = df_bikes['month'].apply(lambda x: calendar.month_abbr[x])
# df_bikes.head()

sns.set_palette("GnBu_d", n_colors=12)
sns.set_palette("colorblind", n_colors=12)

# df_bikes_month = df_bikes.groupby(['month', df_bikes.index.hour])[
#     'age'].count().unstack(level=0)

# fig, axes = plt.subplots(1, 1, figsize=(7, 7), sharex=True)

# df_bikes_month.plot(ax=axes)
# axes.set_ylabel("Concentration (µg/m³)")
# axes.set_xlabel("Heure de la journée")
# axes.set_title(
#     "Profil journalier de la pollution au NO2: effet du weekend?")
# axes.set_xticks(np.arange(0, 24))
# axes.set_xticklabels(np.arange(0, 24), rotation=45)
# # axes.set_ylim(0, 90)
# axes.legend(labels=calendar.month_name[1:], loc='lower left', bbox_to_anchor=(1, 0.1))

# plt.tight_layout()