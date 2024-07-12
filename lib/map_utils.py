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
        data_id = layer.get("config", {}).get("dataId")
        if data_id:
            data_ids.append(data_id)
    return data_ids

# Configura o logging
logging.basicConfig(level=logging.INFO)

def convert_numpy_types(data):
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    elif isinstance(data, gpd.GeoDataFrame):
        return json.loads(data.to_json())
    else:
        return data

def create_kepler_map(geojson_data, config, csv_data=None):
    try:
        kepler_data = {}
        data_ids = get_dataId_from_config(config)

        # Converta os dados para o formato adequado
        if isinstance(geojson_data, gpd.GeoDataFrame):
            geojson_data = convert_numpy_types(geojson_data)
        if csv_data is not None and isinstance(csv_data, pd.DataFrame):
            csv_data = convert_numpy_types(csv_data)

        # Atribua os dados ao KeplerGL
        if len(data_ids) == 1:
            kepler_data[data_ids[0]] = geojson_data
        elif len(data_ids) == 2 and csv_data is not None:
            kepler_data[data_ids[0]] = geojson_data
            kepler_data[data_ids[1]] = csv_data

        print(f"Kepler data: {kepler_data}")
        print(f"Kepler config: {config}")

        kepler_map = KeplerGl(config=config, data=kepler_data)
        
        logging.info(f"Mapa KeplerGL criado com sucesso.")
        return kepler_map._repr_html_()
    except Exception as e:
        logging.error(f"Falha ao criar o mapa KeplerGL: {e}")
        raise
