"""Lidar data."""
import json
import os

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
import pdal
import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist

from logger import Logger


class Lidar:
    def __init__(self, region) -> None:
        """Initialize Lidar Data."""
        self.logger = Logger("load_data.log").get_app_logger()
        self.logger.info("Successfully Instantiated Lidar Class Object")
        self.pipeline_path = "./pipeline.json"
        self.data_path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
        self.input_epsg = "EPSG: 3857"
        self.output_epsg = "EPSG: 4326"
        self.las_name = region.lower() + ".las"
        self.tif_name = region.lower() + ".tif"
        self.region = region
        # pass

    def get_lidar(self, bounds: list) -> None:
        """
        Load pipeline and get bounds for the region.
        Args:
            bounds (list): Bounds list.
        return: None
        
        """

        f_name = self.data_path + self.region + "/ept.json"
        self.logger.info("Getting lidar data json.")
        try:

            with open(self.pipeline_path) as f:
                the_json = json.load(f)

            the_json["pipeline"][0]["filename"] = f_name
            the_json["pipeline"][0]["bounds"] = bounds
            the_json["pipeline"][2]["in_srs"] = self.input_epsg
            the_json["pipeline"][2]["out_srs"] = self.output_epsg
            the_json["pipeline"][3]["filename"] = self.las_name
            the_json["pipeline"][4]["filename"] = self.tif_name
            print(the_json)
            pipeline = pdal.Pipeline(json.dumps(the_json))

            pipeline.execute()
            return pipeline.arrays
        except Exception as e:
            print(e)
            self.logger.error("error loading pipeline")

    def get_elevation(self, bounds) -> None:
        """Get elevation from an array generated in the pipeline.

        Args:
            bounds (list): bound of the polygon
        
        Returns:
            None
        """
        self.logger.info("Getting elevation for each point.")
        arrays = self.get_lidar(bounds)
        for i in arrays:
            geometry_points = [Point(x, y) for x, y in zip(i["X"], i["Y"])]
            elevetions = i["Z"]
            df = gpd.GeoDataFrame(columns=["elevation_m", "Geometry"])
            df["elevation_m"] = elevetions
            df["Geometry"] = geometry_points
            df.set_geometry("Geometry", inplace=True)
            df.set_crs(4326, inplace=True)
            df.to_file("../data/geo.geojson", driver="GeoJSON")
            # df.to_csv("../data/geo.csv")
            self.logger.info("Saved geogson object.")


if __name__ == "__main__":
    # bd = "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])"
    bd = "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])"
    Lidar("IA_FullState").get_elevation(bd)
    # Lidar().raster("../data/iowa.tif")
