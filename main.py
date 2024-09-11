import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.routing import Route, Mount
import geopandas as gpd
import pandas as pd
import os
import json
import logging

# ---- Kepler Configurations ----
from config.shared import read_configs, load_user_config

# ---- Map Libs
from lib.map_utils import create_kepler_map, get_dataId_from_config

# ---- Map Loader
from data.load_data import read_geojsons

# ---- Global Configuration ----
global_config = {"maps": []}
global_maps = {}

# Load configuration from config.json file
user_config = load_user_config()

# Data cache to avoid repeated loads
def cache_data():
    global global_maps
    if not global_maps:
        logging.info("Populating data in cache")
        global_maps = read_geojsons("./data")
    else:
        logging.info("Using cached data")

def create_route_function(map_config):
    async def route_function():
        cache_data()  # Ensure the data is in cache
        geojson_data = {}
        csv_data = {}

        # Check if cache contains data
        if not global_maps:
            return HTMLResponse(content="Missing data file", status_code=404)

        config = map_config["config"]
        if not config:
            return HTMLResponse(content="Map configuration not found", status_code=500)

        # Convert GeoJSON and CSV
        for key, value in global_maps.items():
            if isinstance(value, gpd.GeoDataFrame):
                geojson_data[key] = json.loads(value.to_json())
            elif isinstance(value, pd.DataFrame):
                csv_data[key] = value
            elif isinstance(value, str):
                try:
                    if key.endswith('.geojson'):
                        geojson_data[key] = json.loads(gpd.read_file(value).to_json())
                    elif key.endswith('.csv'):
                        csv_data[key] = pd.read_csv(value)
                except Exception as e:
                    logging.error(f"Error loading file {key}: {e}")
                    global_maps[key] = None

        try:
            # Pass processed data to create_kepler_map
            kepler_html = create_kepler_map(geojson_data, config, csv_data)
            return HTMLResponse(content=kepler_html, status_code=200)
        except Exception as e:
            logging.error(f"Failed to create KeplerGL map: {e}")
            return HTMLResponse(content=f"Error creating map: {e}", status_code=500)

    return route_function

def populate_config():
    cache_data()  # Populate the data cache

    # Adding siteTitle to global_config
    global_config["siteTitle"] = user_config.get("siteTitle", "Default Title")

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

        if data_ids.get('geojson_file') in global_maps or data_ids.get('csv_file') in global_maps:
            global_config["maps"].append({
                "data_ids": data_ids,
                "link": link,
                "label": label,
                "description": map_config.get("description", ""),
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

@app.get("/get_map_info/{map_id}")
async def get_map_info(map_id: str):
    print(f"Received map_id: {map_id}")  # Log to check the received mapId

    for map in global_config["maps"]:
        if 'geojson_file' in map["data_ids"] and map["data_ids"]["geojson_file"].split('.')[0] == map_id:
            print(f"Found map info for geojson_file: {map['data_ids']['geojson_file']}")  # Log to check the geojson file
            return JSONResponse(map)
        elif 'csv_file' in map["data_ids"] and map["data_ids"]["csv_file"].split('.')[0] == map_id:
            print(f"Found map info for csv_file: {map['data_ids']['csv_file']}")  # Log to check the csv file
            return JSONResponse(map)

    print(f"Map info not found for map_id: {map_id}")  # Log if the mapId wasn't found
    raise HTTPException(status_code=404, detail="Map not found")

# ---- Dynamic routes for each map configuration found
for map_config in global_config["maps"]:
    if 'geojson_file' in map_config['data_ids']:
        route = f"/{map_config['data_ids']['geojson_file'].split('.')[0]}"
    elif 'csv_file' in map_config['data_ids']:
        route = f"/{map_config['data_ids']['csv_file'].split('.')[0]}"
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
