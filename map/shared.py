import geopandas as gpd


# Global variable to store data from every different source
data = None


def load_data_nuts_3():
    global data
    data = gpd.read_file("./data/demographic_2020_2030_2040_regions.geojson")
    return data


def load_data_nuts_4():
    global data
    data = gpd.read_file("./data/demographic_2020_2030_2040_mun.geojson")
    return data
