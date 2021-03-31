
import geopandas as gpd
import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt
import contextily as ctx
import branca.colormap as cm
from shapely.geometry import shape

# generate images for the gif, the images are showing intensities of bikes on each counters
# for each day in the data
def images_gif(gdf, dates, ville, df_list):
    numFile=0
    for date in dates:
        print(date)
        ax = ville.plot(figsize = (10, 10), zorder=1, edgecolor='gray', facecolor='none')
        ax.set_title(f"Intensities of bikes in Montpellier at the date {date.year}-{date.month}-{date.day}", fontsize=14, color="dimgray")
        for i in range(len(df_list)):
            if(date in gdf[i].index and len(gdf[i].loc[date].shape)==1):
                current_loc = gpd.GeoDataFrame(gdf[i].loc[date].to_frame().T)
                current_loc.plot(ax = ax, color = 'indianred', alpha = 0.8, zorder = 2, markersize=current_loc["intensity"][date])

        ctx.add_basemap(ax, crs=ville.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_axis_off()
        # plt.title(f"Intensities of bikes at the date {date.year}-{date.month}-{date.day}")
        plt.tight_layout(pad=0)
        #plt.show()
        plt.savefig(f"gifcreation/images/{numFile}.jpg")
        numFile+=1