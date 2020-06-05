import sys
import glob
import collections
import random

import toml

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

static_file_mapping = collections.defaultdict(list)
root_directory = f"{sys.path[0]}".replace("\\", "/")
app = FastAPI()
with open(f"{root_directory}/paths.toml") as toml_file:
    config = toml.load(toml_file)


for path in config["directories"]["directory_paths"]:
    app.mount(f"/{path}", StaticFiles(directory=path), name=path)
    for filename in glob.glob(f"{root_directory}/{path}/*"):
        static_file_mapping[path].append(filename.replace("\\", "/")[1:])

static_file_mapping = dict(static_file_mapping)


@app.get("/random/{name}")
async def return_random(name: str):
    """Returns the URL to a random file in the specified group."""
    result = static_file_mapping.get(name.lower(), None)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No group named {name} found")
    else:
        return {"item": random.choice(result)}
