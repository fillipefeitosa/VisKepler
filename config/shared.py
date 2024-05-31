import json
import os
import geopandas as gpd
from os import listdir
from os.path import isfile, join

# Global variable to store data from every different source
data = None

# I want to make this script read all configuration files
# available.


# Get the list of configuration files
def read_configs(config_path):
    only_files = [f for f in listdir(config_path) if isfile(join(config_path, f))]
    # filter json files
    json_files = [f for f in only_files if f.lower().endswith(".json")]
    configs = []

    for json_file in json_files:
        with open(os.path.join(config_path, json_file), "r") as f:
            config = json.load(f)
            configs.append(config)
    return configs


def load_data_nuts_4():
    global data
    data = gpd.read_file("./data/rs1hiroye.geojson")
    return data


def load_user_config():
    with open("./config/config.json") as f:
        return json.load(f)
