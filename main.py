import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import config.shared as shared
from starlette.routing import Route, Mount
import geopandas as gpd
import pandas as pd

# ---- Kepler Configurations ----
from config import read_configs, load_user_config

# ---- Map Libs
from lib.map_utils import create_kepler_map, get_dataId_from_config

# ---- Map Loader
from data.load_data import read_geojsons

# ---- Global Configuration
# Populate the global config file
global_config = {"maps": []}
global_maps = {}

def create_route_function(map_config):
    async def route_function():
        data_ids = map_config["data_ids"]
        geojson_data = global_maps.get(data_ids['geojson_file'])
        csv_data = global_maps.get(data_ids['csv_file']) if 'csv_file' in data_ids else None
        
        if geojson_data is None or ('csv_file' in data_ids and csv_data is None):
            return HTMLResponse(content="Missing data files", status_code=404)
        
        # Convert data to the appropriate format
        if isinstance(geojson_data, gpd.GeoDataFrame):
            geojson_data = geojson_data.to_json()
        elif isinstance(geojson_data, str):
            geojson_data = gpd.read_file(geojson_data).to_json()
        
        if csv_data is not None:
            if isinstance(csv_data, pd.DataFrame):
                csv_data = csv_data.to_csv(index=False)
            elif isinstance(csv_data, str):
                csv_data = pd.read_csv(csv_data).to_csv(index=False)
        
        config = map_config["config"]
        print(f"Serving map for data_ids: {data_ids}")

        try:
            kepler_html = create_kepler_map(geojson_data, config, csv_data)
            return HTMLResponse(content=kepler_html, status_code=200)
        except Exception as e:
            return HTMLResponse(content=f"Erro ao criar o mapa: {e}", status_code=500)

    return route_function

def populate_config():
    global global_maps
    user_config = load_user_config()
    global_config["siteTitle"] = user_config["siteTitle"]
    global_maps = read_geojsons("./data")

    for map_config in user_config["maps"]:
        data_ids = map_config["data_ids"]
        link = map_config["link"]
        label = map_config["label"]

        config = next(
            (
                config
                for config in read_configs("./config")
                if any(data_id in get_dataId_from_config(config) for data_id in data_ids.values())
            ),
            None,
        )

        if data_ids['geojson_file'] in global_maps and ('csv_file' not in data_ids or data_ids['csv_file'] in global_maps):
            global_config["maps"].append({
                "data_ids": data_ids,
                "link": link,
                "label": label,
                "config": config,
            })

populate_config()

# ---- API ENTRYPOINT ----

app = FastAPI()

app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")

@app.get("/")
async def root():
    return FileResponse("./web/index.html")

@app.get("/get_config")
async def get_config():
    return global_config

# ---- Dynamic routes for each map configuration found
for map_config in global_config["maps"]:
    route = f"/{map_config['data_ids']['geojson_file'].split('.')[0]}"
    print(f"Adding route: {route} for data_ids: {map_config['data_ids']}")  # Log route addition
    app.add_api_route(route, create_route_function(map_config), methods=["GET"])

@app.get("/routes")
async def get_routes():
    routes = []
    for route in app.routes:
        if isinstance(route, Route):
            routes.append(
                {"path": route.path, "name": route.name, "methods": list(route.methods)}
            )
        elif isinstance(route, Mount):
            routes.append(
                {"path": route.path, "name": route.name, "methods": "N/A (Mount)"}
            )
    return {"routes": routes}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8050, reload=True)
