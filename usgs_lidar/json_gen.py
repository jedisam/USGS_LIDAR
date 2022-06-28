"""Generate json data."""
# aws s3 ls s3://usgs-lidar-public/ --no-sign-request

from logger import Logger
import json


class DataGen:
    def __init__(self) -> None:
        """Initialize Datagen."""
        self.logger = Logger("data_gen.log").get_app_logger()
        self.logger.info("Successfully Instantiated Data_gen Class Object")

    def generate_json(self, dest) -> None:
        """
        Generate json data of all regions.
        
        Args:
            dest (str): destionation path of genrated data.
        
        Returns:
            None
        """
        dict_reg = {}
        with open("rg_year.txt", "r") as f:
            ind = 1
            for line in f:
                dict_reg[ind] = line.replace(" ", "").replace('"', "").replace("\n", "")
                ind = ind + 1
                # break

        with open(dest, "w") as f:
            json.dump(dict_reg, f)
