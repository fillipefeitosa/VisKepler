import json
import geopandas as gpd
from os import listdir
from os.path import isfile, join

# Global variable to store data from every different source
data = None

# I want to make this folder and script to read all configuration files
# available. 

# Get the list of configuration files
def read_configs():
    config_path = '.'
    only_files = [f for f in listdir(config_path) if isfile(join(config_path, f))]
    # filter json files
    json_files = [f for f in only_files if f.lower.endswith('.json')]
    return json_files

# Read each config file
def load_configs():
    config_files = read_configs()
    for e in config_files:
        with open(e) as f:
            conf = json.load(f)
            
            

def load_data_nuts_3():
    global data
    data = gpd.read_file("./data/demographic_2020_2030_2040_regions.geojson")
    return data


def load_data_nuts_4():
    global data
    data = gpd.read_file("./data/demographic_2020_2030_2040_mun.geojson")
    return data
