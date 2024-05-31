import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import config.shared as shared
from starlette.routing import Route, Mount

# ---- Kepler Configurations ----
from config import read_configs, load_user_config

# ---- Map Libs
from lib.map_utils import create_kepler_map, get_dataId_from_config

# ---- Map Loader
from data import read_geojsons


# ---- Global Configuration
# Populate the global config file
global_config = {"maps": []}
global_maps = {}


def create_route_function(map_config):
    async def route_function():
        data_id = map_config["data_id"]
        geojson = global_maps[f"{data_id}.geojson"]
        config = map_config["config"]
        print(f"Serving map for data_id: {data_id}")

        kepler_html = create_kepler_map(geojson, config)
        return HTMLResponse(content=kepler_html, status_code=200)

    return route_function


def populate_config():
    global global_maps
    user_config = load_user_config()
    global_config["siteTitle"] = user_config["siteTitle"]
    # Also responsable to load map data
    global_maps = read_geojsons("./data")

    for map_config in user_config["maps"]:
        data_id = map_config["data_id"]
        geojson_file = map_config["geojson_file"]
        link = map_config["link"]
        label = map_config["label"]

        print(
            f"Loading config for data_id: {data_id}, geojson_file: {geojson_file}"
        )  # Log file loading
        if geojson_file in global_maps:
            global_config["maps"].append(
                {
                    "data_id": data_id,
                    "geojson": geojson_file,
                    "link": link,
                    "label": label,
                    "config": next(
                        (
                            # Find the first configuration that contains the current data_id in its list of data IDs.
                            # If no such configuration is found, return None.
                            config
                            for config in read_configs("./config")
                            if data_id in get_dataId_from_config(config)
                        ),
                        None,
                    ),
                }
            )


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


# ---- Dynamic routes for each map configuration found
for map_config in global_config["maps"]:
    data_id = map_config["data_id"]
    route = f"/{data_id}"
    print(f"Adding route: {route} for data_id: {data_id}")  # Log route addition
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
