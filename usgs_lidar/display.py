"""Visualiztion of dataframe."""
import matplotlib.pyplot as plt
import geopandas as gpd
import laspy as lp
import numpy as np
import pandas as pd

point_cloud = lp.read("../data/ia_fullstate.las")

colors = np.vstack((point_cloud.red, point_cloud.green, point_cloud.blue)).transpose()


def plot_3d(df) -> None:
    """Plot 3d map of input dataframe.

    Args:
        (GeoDataFRame): GeoDataframe to be displayed.
    return: None

    """
    if df["elevation_m"][0] != None:
        gdf = df
        gdf.crs = "epsg:4326"
        # print("THE GEOOOOOOOOOOOO: ", gdf.geometry)

    x = gdf.geometry.x
    y = gdf.geometry.y
    z = gdf.elevation_m
    points = np.vstack((x, y, z)).transpose()
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


# df = pd.read_csv("../data/geo.csv")
df = gpd.read_file("../data/geo.geojson")
plot_3d(df)
