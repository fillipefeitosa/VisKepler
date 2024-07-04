import os
import geopandas as gpd
import pandas as pd

def read_geojsons(directory):
    geojsons = {}
    for file in os.listdir(directory):
        if file.endswith('.geojson'):
            file_path = os.path.join(directory, file)
            try:
                geojsons[file] = gpd.read_file(file_path)
            except UnicodeDecodeError as e:
                print(f"Error decoding file {file_path}: {e}")
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        elif file.endswith('.csv'):
            file_path = os.path.join(directory, file)
            try:
                geojsons[file] = pd.read_csv(file_path)
            except Exception as e:
                print(f"Error reading CSV file {file_path}: {e}")
    return geojsons
