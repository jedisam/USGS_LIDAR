import numpy as np
import laspy as lp
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# from get_data import get_geopandas_dataframe
import geopandas as gpd
import os


point_cloud = lp.read("SoPlatteRiver" + ".las")

colors = np.vstack((point_cloud.red, point_cloud.green, point_cloud.blue)).transpose()


def plot_3d_map(df=None):
    """Plots 3d map of input dataframe
    Arguments: df, takes in dataframe 
    return: None
    """
    if df["elevation_m"][0] != None:
        gdf = df
        gdf.crs = "epsg:4326"

    x = gdf.geometry.x
    y = gdf.geometry.y
    z = gdf.elevation_m
    points = np.vstack((x, y, z)).transpose()
    factor = 160
    decimated_points = points[::]
    decimated_colors = colors[::]
    print(len(decimated_colors))
    print(decimated_colors)
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax = plt.axes(projection="3d")
    ax.scatter(
        decimated_points[:, 0],
        decimated_points[:, 1],
        decimated_points[:, 2],
        s=0.01,
        color=decimated_colors / 255,
    )
    plt.show()


df = gpd.read_file("../data/geo.geojson")
plot_3d_map(df)
