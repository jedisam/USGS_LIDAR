"""Load data from AWS dataset."""

import json
import sys
from urllib.request import urlopen

import pandas as pd
from progress.bar import Bar

from logger import Logger


class LoadData:
    def __init__(self) -> None:
        """Initialize loaddata class."""
        try:
            self.logger = Logger("load_data.log").get_app_logger()
            self.logger.info("Successfully Instantiated LoadData Class Object")
            self.data_path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
            self.df = pd.DataFrame(
                columns=[
                    "region",
                    "year",
                    "xmin",
                    "xmax",
                    "ymin",
                    "ymax",
                    "zmin",
                    "zmax",
                    "points",
                ]
            )
        except Exception:
            self.logger.exception("Failed to Instantiate Preprocessing Class Object")
            sys.exit(1)

    def get_regions(self, regions) -> None:
        """
        Get the regions data from a json file.
        
        return: None
        """
        with open(regions, "r") as f:
            self.regions = json.load(f)
            self.bar = Bar("Loading MetaData", max=len(self.regions))

    def get_data(self, regions) -> None:
        """
        Get boundaries of the data.
        
        Args:
            regions(str): path to regions json file
        
        return: None
        """
        # Get the regions
        self.get_regions(regions)
        # print(len(self.regions))
        data = []
        for ind in range(len(self.regions)):
            try:
                self.logger.info("Started loading metadata...")
                # print(self.regions[str(ind + 1)])
                end_pt = self.data_path + self.regions[str(ind + 1)] + "/ept.json"
                res = json.loads(urlopen(end_pt).read())
            except Exception as e:
                print("The status: ", res)
                print(e)
                self.logger.error("Error loading file")
            if res:
                x = {
                    "region": "".join(self.regions[str(ind + 1)]),
                    "year": self.regions[str(ind + 1)].split("_")[-1],
                    "xmin": res["bounds"][0],
                    "xmax": res["bounds"][3],
                    "ymin": res["bounds"][1],
                    "ymax": res["bounds"][4],
                    "zmin": res["bounds"][2],
                    "zmax": res["bounds"][5],
                    "points": res["points"],
                }

                data.append(x)
                self.bar.next()
            else:
                pass
        self.df = pd.DataFrame(data)
        self.bar.finish()
        self.logger.info("Successfully loaded metadata.")
        self.save_csv("../data/metadata.csv")

    def save_csv(self, path) -> None:
        """Save dataframe as a csv.

        Args:
            path (str): path of the csv file
            
        return:
            None
        """
        try:
            self.df.to_csv(path, index=False)
        except Exception as e:
            print(e)
            self.logger.error("Failed to save file to csv")


if __name__ == "__main__":
    LoadData().get_data()
