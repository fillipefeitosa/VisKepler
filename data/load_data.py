from os import listdir
import os
from os.path import isfile, join
import geopandas as gpd

def read_geojsons(data_path):
    only_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    # filter the geojson files
    geojson_files = [f for f in only_files if f.lower().endswith('.geojson')]
    
    geojsons = {}
    for geojson_file in geojson_files:
        with open(os.path.join(data_path, geojson_file), 'r') as f:
            geojsons[geojson_file] = gpd.read_file(f)
            
    return geojsons