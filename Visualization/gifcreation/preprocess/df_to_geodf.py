from shapely.geometry import shape
import geopandas as gpd

# Changing dataframe format to Geodataframe for each dataframe in df_list 
def df_to_geodf(df_list):
    gdf=[]
    for i in range(len(df_list)):
        df_list[i]['location'] = df_list[i]['location'].apply(shape)
        gdf.append(gpd.GeoDataFrame(df_list[i]))
        gdf[i]["geometry"] = gdf[i]['location']
    return gdf