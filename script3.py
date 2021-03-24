
# %%
import bikevisualization as bv
import pandas as pd
import numpy as np
import string, os
import matplotlib.pyplot as plt
import requests, tempfile, zipfile
import urllib, json
import seaborn as sns
from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


#%%

df_counters = bv.Load_json().save_as_df()

#%%
days =  ['Lundi', 'Mardi', 'Mercredi',
        'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

#%%
# for i in range(10) : 
#     column_index = df_counters[i].columns
#     for j in df_counters[i].index :
#         df_counters[i]["date"] = pd.to_datetime(df_counters[i]["dateObserved"][j][0:10], format="%Y-%m-%d")
#         #df_counters[i]["weekday"] = df_counters[i]["date"][j].weekday

#%%

sns.set_palette("GnBu_d", n_colors=7)
counter_week = df_counters[0].groupby(['weekday', df_counters[0]["date"].dt.hour])["intensity"].mean().unstack(level=0)


fig, axes = plt.subplots(2, 1, figsize=(7, 7), sharex=True)

counter_week.plot(ax=axes[0])
axes[0].set_ylabel("Concentration (µg/m³)")
axes[0].set_xlabel("Heure de la journée")
axes[0].set_title(
    "Profil journalier de la pollution au NO2: effet du weekend?")
axes[0].set_xticks(np.arange(0, 24))
axes[0].set_xticklabels(np.arange(0, 24), rotation=45)
axes[0].set_ylim(0, 60)

axes[0].legend().set_visible(False)
# ax.legend()
axes[1].legend(labels=days, loc='lower left', bbox_to_anchor=(1, 0.1))

plt.tight_layout()



#%%

for i in range(10) : 
    df_counters[i] = df_counters[i].assign(date = 0)
    df_counters[i] = df_counters[i].assign(weekday = 0)

     #df_counters[i] = df_counters[i].assign(end_date = 0)
    column_index = df_counters[i].columns
    for j in df_counters[i].index :
        df_counters[i].iloc[j, column_index.get_loc("date")] = pd.to_datetime(df_counters[i].iloc[j,column_index.get_loc("dateObserved")][0:10], format="%Y-%m-%d")
        #df_counters[i].iloc[j, column_index.get_loc("end_date")] = pd.to_datetime(df_counters[i].iloc[j,column_index.get_loc("dateObserved")][20:30], format="%Y-%m-%d")
        #df_counters[i]['weekday'] = df_counters["date"].weekday  # Monday=0, Sunday=6



#%%
def relplot_counter(dict_counters, counter):
    sns.set_theme(style="darkgrid")
    #sns.lineplot(x="begin_date", y="intensity", data=dict_counters[counter])
    sns.relplot(x="date", y="intensity", kind="line", ci="sd", data=dict_counters[counter])
    plt.xlabel('Date')
    plt.ylabel('Nombre de vélos (Intensité)')
    plt.title("Nombre de vélos en fonction de la date")
    plt.tight_layout()
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

dict_counters = {}
i = 0
for elt in counters:
    dict_counters[elt] = df_counters[i]
    i = i + 1

#%%
interact(relplot_counter, dict_counters = fixed(dict_counters), counter=counters);


# %%

def histplot_counter(dict_counters, counter):
    sns.histplot(dict_counters[counter]["intensity"])


interact(histplot_counter, dict_counters = fixed(dict_counters), counter=counters);

# %%

def hist_explore(counter, alpha=0.25, density=False):
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.hist(df_titanic['Age'], density=density,
            bins=n_bins, alpha=0.25)  # standardization
    plt.xlabel('Age')
    plt.ylabel('Density level')
    plt.title("Histogram for passengers' age")
    plt.tight_layout()
    plt.show()

interact(hist_explore, counter=counters, week=(1, 50, 1), density=False)


#%%

sns.set_palette("colorblind")
sns.catplot(x='Pclass',y='Age',hue='Survived',data=df_titanic_raw, kind="violin")

#%%


