"""Lidar data."""
import json
import os

import geopandas as gpd
import pandas as pd
import pdal

from logger import Logger


class Lidar:
    def __init__(self) -> None:
        """Initialize Lidar Data."""
        self.logger = Logger("load_data.log").get_app_logger()
        self.logger.info("Successfully Instantiated Lidar Class Object")
        self.pipeline_path = "./pipeline.json"
        self.data_path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
        self.input_epsg = "EPSG: 3857"
        self.output_epsg = "EPSG: 4326"
        pass

    def get_lidar(self, bound: list, region: str):
        """Load pipeline and get bounds for the region."""
        f_name = self.data_path + region + "/ept.json"
        try:
            with open(self.pipeline_path) as f:
                the_json = json.load(f)

            the_json["pipeline"][0]["filename"] = f_name
            the_json["pipeline"][0]["bounds"] = bound
            the_json["pipeline"][2]["in_srs"] = self.input_epsg
            the_json["pipeline"][2]["out_srs"] = self.output_epsg

            pipeline = pdal.Pipeline(json.dumps(the_json))

            pipeline.execute()
        except Exception as e:
            print(e)
            self.logger.error("error loading pipeline")


if __name__ == "__main__":
    bd = "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])"
    Lidar().get_lidar(bd, "IA_FullState")
