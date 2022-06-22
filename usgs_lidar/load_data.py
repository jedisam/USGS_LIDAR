"""Load data from AWS dataset."""

import json
import sys

# import pdal

from logger import Logger


class LoadData:
    def __init__(self) -> None:
        """Initialize loaddata class."""
        try:
            self.logger = Logger("load_data.log").get_app_logger()
            self.logger.info("Successfully Instantiated LoadData Class Object")
        except Exception:
            self.logger.exception("Failed to Instantiate Preprocessing Class Object")
            sys.exit(1)

    def get_regions(self):
        """Get the regions data from a json file."""
        with open("regions.json", "r") as f:
            self.regions = json.load(f)


if __name__ == "__main__":
    LoadData().get_regions()
