import logging
from keplergl import KeplerGl


def get_dataId_from_config(config):
    # Uses KeplerGl config to get the dataId. Can return multiple dataIds
    data_ids = []
    layers = config.get("config", {}).get("visState", {}).get("layers", [])
    for layer in layers:
        data_id = layer.get("config", {}).get("dataId")
        if data_id:
            data_ids.append(data_id)
    return data_ids


# Set up logging
logging.basicConfig(level=logging.INFO)


def create_kepler_map(data, config):
    try:
        dataIds = get_dataId_from_config(config)
        # One day we might want to support multiple dataIds
        if len(dataIds) != 1:
            raise ValueError(
                "Only one dataId allowed. You probably have multiple layers with different dataIds or no dataId at all."
            )
        dataId = dataIds[0]
        kepler_map = KeplerGl(config=config, data={dataId: data})

        logging.info(f"KeplerGL map for dataId {dataId} successfully created.")
        return kepler_map._repr_html_()
    except Exception as e:
        logging.error(f"Failed to create KeplerGL map: {e}")
        raise
