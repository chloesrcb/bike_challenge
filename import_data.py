
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from download import download 
import seaborn as sns
from ipywidgets import interact 

#%%
# url1 ='https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv'
# path_target = "./data_bike.csv"
# download(url1, path_target, replace=True)
df_bike = pd.read_csv("data_bike.csv")
df_bike.columns = ['Date', 'Heure', 'Grand total', 'Total jour', 'Remarque']


#%%
print(df_bike.describe())

# %%

plt.figure(figsize=(5, 5))
plt.hist(df_bike['Grand total'], density=True, bins=50)
plt.xlabel('Total de vélos depuis le 1er janvier')
plt.ylabel('Proportion')
plt.title("Histogramme du nombre de vélos depuis le 1er janvier")

# %%
plt.figure(figsize=(5, 5))
plt.hist(df_bike['Total jour'], density=True, bins=50)
plt.xlabel('Total de vélos par jour')
plt.ylabel('Proportion')
plt.title("Histogramme du nombre de vélos par jour")

# %%

plt.figure(figsize=(5, 5), num='jfpwje')
ax = sns.kdeplot(df_bike['Grand total'], shade=True, cut=0, bw=0.2)
plt.xlabel('Proportion')
plt.ylabel('Grand total')
ax.legend().set_visible(False)
plt.title("Estimation de la densité du total de nombre de vélos")
plt.tight_layout()

# %%
