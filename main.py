import uvicorn
from keplergl import KeplerGl
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import map.shared as shared

# ---- Kepler Configurations ----
from map.config_nuts4 import config_nuts4
from map.config_nuts3 import config_nuts3

# Next Changes
# 1. Load kepler configurations available
# 2. Load the geojsons available


def get_dataId_from_config(config):
    # Uses KeplerGl config to get the dataId. Can return multiple dataIds
    data_ids = []
    layers = config.get("config", {}).get("visState", {}).get("layers", [])
    for layer in layers:
        data_id = layer.get("config", {}).get("dataId")
        if data_id:
            data_ids.append(data_id)
    return data_ids


def create_kepler_map(data, config):
    dataIds = get_dataId_from_config(config)
    # One day we might want to support multiple dataIds
    if len(dataIds) != 1:
        raise ValueError(
            "Only one dataId allowed. You probably have multiple layers with different dataIds or no dataId at all."
        )
    dataId = dataIds[0]
    kepler_map = KeplerGl(config=config, data={dataId: data})
    return kepler_map._repr_html_()


# ---- API ENTRYPOINT ----

app = FastAPI(root_path="/kepler-pt-demo")


app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")


@app.get("/")
async def root():
    return FileResponse("./web/index.html")


@app.get("/nuts4")
async def nuts4():
    data_nuts4 = shared.load_data_nuts_4()
    kepler_html = create_kepler_map(data_nuts4, config_nuts4)
    return HTMLResponse(content=kepler_html, status_code=200)


@app.get("/nuts3")
async def nuts3():
    data_nuts3 = shared.load_data_nuts_3()
    kepler_html = create_kepler_map(data_nuts3, config_nuts3)
    return HTMLResponse(content=kepler_html, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8050, reload=True)
