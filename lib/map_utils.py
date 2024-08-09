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

def create_kepler_map(geojson_data, config, csv_data=None, additional_data=None):
    try:
        kepler_data = {}
        data_ids = get_dataId_from_config(config)
        
        # Garantir que additional_data é uma lista válida
        if additional_data is None:
            additional_data = []
        
        for i, data_id in enumerate(data_ids):
            if i == 0 and geojson_data is not None:
                kepler_data[data_id] = geojson_data
            elif i == 1 and csv_data is not None:
                kepler_data[data_id] = csv_data
            elif i >= 2 and i-2 < len(additional_data):
                kepler_data[data_id] = additional_data[i-2]  # Adiciona dados adicionais
            else:
                logging.warning(f"Data not found for dataId {data_id}")

        kepler_map = KeplerGl(config=config, data=kepler_data)
        logging.info("Mapa KeplerGL criado com sucesso.")
        return kepler_map._repr_html_()
    except Exception as e:
        logging.error(f"Falha ao criar o mapa KeplerGL: {e}")
        raise

