import uvicorn
from keplergl import KeplerGl
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import config.shared as shared
from starlette.routing import Route, Mount

# ---- Kepler Configurations ----
from config.config_nuts4 import config_nuts4
from config.config_nuts3 import config_nuts3
from config import read_configs

# ---- Map Loader
from data import read_geojsons

# Next Changes
# 1. Load kepler configurations available - ok
# 2. Load the geojsons available - ok - I can read the geojsons name
# - Now I need to to read the available config.jsons
# - Finally, I will need to create a general config file, that 
# will link the geojsons with their configurations


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

def create_route_function(map_config):
    async def route_function():
        data_id = map_config['data_id']
        geojson = global_maps[f"{data_id}.geojson"]
        config = map_config['config']
        
        kepler_html = create_kepler_map(geojson, config)
        return HTMLResponse(content=kepler_html, status_code=200)
    return route_function

# ---- Global Configuration
# Populate the global config file        
global_config = {
    "maps": []
}
global_maps = {}
def populate_config():
    global global_maps
    config_path = "./config"
    data_path = "./data"
    configs = read_configs(config_path)
    # Also responsable to load map data
    global_maps = read_geojsons(data_path)
    
    for config in configs:
        data_ids = get_dataId_from_config(config)
        # ATTENTION: For now only one dataID is supported
        for data_id in data_ids:

            geojson_file = f"{data_id}.geojson"
            if geojson_file in global_maps:
                global_config["maps"].append({
                    "data_id": data_id,
                    "geojson": geojson_file,
                    "link": f"/{data_id}",
                    "config": config,
                    
                })

populate_config()

# ---- API ENTRYPOINT ----

app = FastAPI(root_path="/kepler-pt-demo")


app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")


@app.get("/")
async def root():
    return FileResponse("./web/index.html")

@app.get("/get_config")
async def get_config():
    return global_config

@app.get("/nuts4")
async def nuts4():
    data_nuts4 = shared.load_data_nuts_4()
    kepler_html = create_kepler_map(data_nuts4, config_nuts4)
    return HTMLResponse(content=kepler_html, status_code=200)

# ---- Dynamic routes for each map configuration found
for map_config in global_config["maps"]:
    data_id = map_config['data_id']
    route = f"/{data_id}"

    app.add_api_route(route, create_route_function(map_config), methods=['GET'])

@app.get("/routes")
async def get_routes():
    routes = []
    for route in app.routes:
        if isinstance(route, Route):
            routes.append({
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods)
            })
        elif isinstance(route, Mount):
            routes.append({
                "path": route.path,
                "name": route.name,
                "methods": "N/A (Mount)"
            })
    return {"routes": routes}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8050, reload=True)

