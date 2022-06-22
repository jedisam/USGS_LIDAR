# USGS LIDAR

<!-- Table of contents -->
- [USGS LIDAR](#usgs-lidar)
  - [About](#about)
  - [Objectives](#objectives)
  - [Data](#data)
  - [Repository overview](#repository-overview)
  - [Requirements](#requirements)
  - [Contrbutors](#contrbutors)
  - [Contributing](#contributing)
  - [License](#license)

## About
At AgriTech, we are very interested in how water flows through a maize farm field. This knowledge will help us improve our research on new agricultural products being tested on farms.

How much maize a field produces is very spatially variable. Even if the same farming practices, seeds and fertilizer are applied exactly the same by machinery over a field, there can be a very large harvest at one corner and a low harvest at another corner.  We would like to be able to better understand which parts of the farm are likely to produce more or less maize, so that if we try a new fertilizer on part of this farm, we have more confidence that any differences in the maize harvest 9are due mostly to the new fertilizer changes, and not just random effects due to other environmental factors.

Water is very important for crop growth and health.  We can better predict maize harvest if we better understand how water flows through a field, and which parts are likely to be flooded or too dry. One important ingredient to understanding water flow in a field is by measuring the elevation of the field at many points. 



## Objectives
As a data engineering, the goal is to produce an easy to use, reliable and well designed python module that domain experts and data scientists can use to fetch, visualise, and transform publicly available satellite and LIDAR data. The code should interface with USGS 3DEP and fetch data using their API. 


## Data
The USGS recently released high resolution elevation data as a lidar point cloud called USGS 3DEP in a public dataset on Amazon. This dataset is essential to build models of water flow and predict plant health and maize harvest. It can be found [here](https://www.usgs.gov/core-science-systems/ngp/3dep)


## Repository overview
 Structure of the repository:
 
        ├── .github  (github workflows for CI/CD)
        ├── data    (contains data from aws wich contains the entwine formats as well as laz)
        ├── usgs_lidar (contains the script)	
        |   ├── logger.py (logger for the project)
        |   ├── json_gen.py (Generate the json data of available regions)
        |   ├── load_data.py (Loads the data and required metadata)
        |   ├── regions.json (avialable regions in json format)
        |   ├── preprocess.py (Data preprocessing)
        ├── notebooks	
        ├── tests 
        │   ├── test_preprocess.py (test prep)
        ├── README.md (contains the project description)
        ├── requirements.txt (contains the required packages)
        |── LICENSE (license of the project)
        └── setup.py (contains the setup of the project)

## Requirements
The project requires the following:
python3
Pip3

## Contrbutors
- Yididiya Samuel

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)
