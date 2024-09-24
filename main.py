import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.routing import Route, Mount
import geopandas as gpd
import pandas as pd
import os
import json

# ---- Kepler Configurations ----
from config.shared import read_configs, load_user_config

# ---- Map Libraries ----
from lib.map_utils import create_kepler_map, get_dataId_from_config

# ---- Map Loader ----
from data.load_data import read_geojsons

# ---- Global Configuration ----
global_config = {"maps": []}
global_maps = {}

# Load user configuration from the config.json file
user_config = load_user_config()

# Function to create a dynamic route for each map configuration
def create_route_function(map_config):
   async def route_function():
       data_ids = map_config["data_ids"]
       geojson_data = global_maps.get(data_ids.get('geojson_file'))
       csv_data = global_maps.get(data_ids.get('csv_file')) if 'csv_file' in data_ids else None

       # Check if the required data files are available
       if geojson_data is None and csv_data is None:
           return HTMLResponse(content="Missing data file", status_code=404)

       # Convert GeoJSON data to the appropriate format
       if geojson_data is not None:
           if isinstance(geojson_data, gpd.GeoDataFrame):
               geojson_data = geojson_data.to_json()
           elif isinstance(geojson_data, str):
               geojson_data = gpd.read_file(geojson_data).to_json()

       # Convert CSV data to the appropriate format
       if csv_data is not None:
           if isinstance(csv_data, pd.DataFrame):
               csv_data = csv_data.to_csv(index=False)
           elif isinstance(csv_data, str):
               csv_data = pd.read_csv(csv_data).to_csv(index=False)

       # Support for additional data files if available
       additional_data = []
       for key, value in data_ids.items():
           if key not in ['geojson_file', 'csv_file']:
               additional_data.append(global_maps.get(value))

       config = map_config["config"]
       print(f"Serving map for data_ids: {data_ids}")

       try:
           # Create and serve the Kepler map with the given data and configuration
           kepler_html = create_kepler_map(geojson_data, config, csv_data, additional_data)
           return HTMLResponse(content=kepler_html, status_code=200)
       except Exception as e:
           return HTMLResponse(content=f"Error creating the map: {e}", status_code=500)

   return route_function

# Function to populate the global configuration and load map data
def populate_config():
   global global_maps
   global_maps = read_geojsons("./data")

   # Adding siteTitle to global_config from user configuration
   global_config["siteTitle"] = user_config.get("siteTitle", "Default Title")

   # Loop through each map configuration from user config
   for map_config in user_config["maps"]:
       data_ids = map_config["data_ids"]
       link = map_config["link"]
       label = map_config["label"]

       # Find the corresponding configuration from available configs
       config = next(
           (
               config
               for config in read_configs("./config")
               if any(data_id in get_dataId_from_config(config) for data_id in data_ids.values())
           ),
           None,
       )

       # Check if data files exist in global maps and add to the global configuration
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

# Endpoint to get the global configuration
@app.get("/get_config")
async def get_config():
   return global_config

# Endpoint to retrieve specific map information by map_id
@app.get("/get_map_info/{map_id}")
async def get_map_info(map_id: str):
   print(f"Received map_id: {map_id}")  # Log to check the received mapId

   # Loop through all maps to find the requested map information
   for map in global_config["maps"]:
       if 'geojson_file' in map["data_ids"] and map["data_ids"]["geojson_file"].split('.')[0] == map_id:
           print(f"Found map info for geojson_file: {map['data_ids']['geojson_file']}")  # Log for GeoJSON file
           return JSONResponse(map)
       elif 'csv_file' in map["data_ids"] and map["data_ids"]["csv_file"].split('.')[0] == map_id:
           print(f"Found map info for csv_file: {map['data_ids']['csv_file']}")  # Log for CSV file
           return JSONResponse(map)

   print(f"Map info not found for map_id: {map_id}")  # Log if mapId was not found
   raise HTTPException(status_code=404, detail="Map not found")

# ---- Create dynamic routes for each map configuration ----
for map_config in global_config["maps"]:
   if 'geojson_file' in map_config['data_ids']:
       route = f"/{map_config['data_ids']['geojson_file'].split('.')[0]}"
   elif 'csv_file' in map_config['data_ids']:
       route = f"/{map_config['data_ids']['csv_file'].split('.')[0]}"
   print(f"Adding route: {route} for data_ids: {map_config['data_ids']}")  # Log route addition
   app.add_api_route(route, create_route_function(map_config), methods=["GET"])

# Endpoint to list all available routes
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
