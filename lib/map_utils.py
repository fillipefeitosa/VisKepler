import json
import logging
from keplergl import KeplerGl
import geopandas as gpd
import pandas as pd

def get_dataId_from_config(config):
    if config is None:
        return []
    data_ids = []
    layers = config.get("config", {}).get("visState", {}).get("layers", [])
    for layer in layers:
        data_id = layer["config"]["dataId"]
        if data_id:
            data_ids.append(data_id)
    return data_ids

# Configure logging
logging.basicConfig(level=logging.INFO)

def convert_numpy_types(data):
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    elif isinstance(data, gpd.GeoDataFrame):
        return json.loads(data.to_json())
    else:
        return data

def create_kepler_map(geojson_data, config, csv_data=None, additional_data=None):
    try:
        kepler_data = {}
        
        # Process layers according to the configuration
        for layer in config["config"]["visState"]["layers"]:
            data_id = layer["config"]["dataId"]
            
            if data_id in geojson_data:
                kepler_data[data_id] = geojson_data[data_id]
                logging.info(f"GeoJSON data added for {data_id}")
            elif data_id in csv_data:
                kepler_data[data_id] = csv_data[data_id]
                logging.info(f"CSV data added for {data_id}")
            else:
                logging.warning(f"No data found for {data_id}. Check if the data is correctly loaded.")
        
        # Ensure at least one layer is added
        if not kepler_data:
            raise ValueError("No GeoJSON or CSV layer was added. Check the data and configuration.")

        # Create the map with the processed layers
        kepler_map = KeplerGl(config=config, data=kepler_data)
        logging.info("KeplerGL map created successfully.")
        return kepler_map._repr_html_()
    
    except Exception as e:
        logging.error(f"Failed to create KeplerGL map: {e}")
        raise
