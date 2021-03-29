
# %%
import bikevisualization as bv
import pandas as pd
import numpy as np
import string, os
import matplotlib.pyplot as plt
import requests, tempfile, zipfile
import urllib, json
import seaborn as sns
#from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
import calendar

#%%

# load data in a list of dataframe
df_counters = bv.Load_json().save_as_df()

#%%

# format data for all dataframe in df_counters
df_counters = bv.format_dfs(df_counters)

#%% 
counters = [
    "Berracasa",
    "Laverune",
    "Celleneuve",
    "Lattes 2",
    "Lattes 1",
    "Vieille Poste",
    "Gerhardt",
    "Albert 1er",
    "Delmas 1",
    "Delmas 2"
    ]

dict_counters = bv.create_dict_counter(counters, df_counters)

#%%
interact(bv.plot_counter, dict_counters = fixed(dict_counters), counter=counters, date=False, week=False, month=False, histogram=False);

# %%
interact(bv.plot_counter, dict_counters = fixed(dict_counters), counter=counters, option=["date","week","month","histogram", "animation"], animation=False)