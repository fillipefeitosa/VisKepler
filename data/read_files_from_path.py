from os import listdir
from os.path import isfile, join

def read_files_from_path(path):
    only_files = [f for f in listdir(path) if isfile(join(path, f))]
    # filter the geojson files
    geojson_files = [f for f in only_files if f.lower().endswith('.geojson')]
    return geojson_files