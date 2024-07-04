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
        dataIds = get_dataId_from_config(config)
        
        if len(dataIds) not in [1, 2]:
            raise ValueError(
                "Esperado um ou dois dataId(s): um para geojson e opcionalmente um para csv."
            )

        kepler_data = {dataIds[0]: convert_numpy_types(geojson_data)}
        if csv_data is not None and len(dataIds) == 2:
            kepler_data[dataIds[1]] = convert_numpy_types(csv_data)
        
        kepler_map = KeplerGl(config=config, data=kepler_data)
        
        logging.info(f"Mapa KeplerGL criado com sucesso para dataIds: {dataIds}.")
        return kepler_map._repr_html_()
    except Exception as e:
        logging.error(f"Falha ao criar o mapa KeplerGL: {e}")
        raise
