# misc: miscellaneous helper functions/classes

import json
import numpy as np
import os
import pandas as pd
from io import StringIO

# JSON encoder for numpy types
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

# export dict containing numpy values to json
def export_json(obj, filename:str):
    json_str = json.dumps(obj, indent=4, cls=NpEncoder)
    with open(filename, "w") as file:
        assert(file.write(json_str) == len(json_str))

# import dict from json
def import_json(filename:str) -> dict:
    with open(filename) as file:
        return json.loads(file.read())

# dump dataframe to stdout
def dump_df(df: pd.DataFrame, header: str):
    print(header)
    print(df)
    print("\n\n\n")

# make dataframe from file contents
def make_df(file: str | StringIO):
    return pd.DataFrame(pd.read_csv(file))

# maybe mkdir depending on if it already exists or not
def maybe_mkdir(path: str) -> None:
    if os.path.isdir(path):
        return
    try:
        _ = os.stat(path)
        assert(False)
    except FileNotFoundError:
        os.mkdir(path)

