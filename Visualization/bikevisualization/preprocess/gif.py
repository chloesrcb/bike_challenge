import pandas as pd
import numpy as np
import string, os
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
import branca.colormap as cm
from shapely.geometry import shape

# Changing dataframe format to Geodataframe for each dataframe in df_list 
def df_to_geodf(df_list):
    gdf=[]
    for i in range(len(df_list)):
        df_list[i]['location'] = df_list[i]['location'].apply(shape)
        gdf.append(gpd.GeoDataFrame(df_list[i]))
        gdf[i]["geometry"] = gdf[i]['location']
    return gdf


# create a list of dates from df_list
def date_list(df_list):
    dates = []
    for i in range(len(df_list)):
        dates = list(set(dates) | set(df_list[i].index))
    dates.sort()
    return dates


# generate images for the gif, the images are showing intensities of bikes on each counters
# for each day in the data
def images_gif(ville, df_list):
    gdf = df_to_geodf(df_list)
    dates = date_list(df_list)
    numFile=0
    for date in dates:
        print(date)
        ax = ville.plot(figsize = (10, 10), zorder=1, edgecolor='black', facecolor='none', color=None)
        for i in range(len(df_list)):
            if(date in gdf[i].index and len(gdf[i].loc[date].shape)==1):
                current_loc = gpd.GeoDataFrame(gdf[i].loc[date].to_frame().T)
                current_loc.plot(ax = ax, color = 'red', alpha = 0.8, zorder = 2, markersize=current_loc["intensity"][date])

        ctx.add_basemap(ax, crs=ville.crs.to_string(), source=ctx.providers.Stamen.Watercolor)
        ax.set_axis_off()
        plt.title(f"Intensities of bikes at the date {date.year}-{date.month}-{date.day}")
        plt.tight_layout(pad=0)
        #plt.show()
        plt.savefig(f"bikevisualization/images/{numFile}.jpg")
        numFile+=1