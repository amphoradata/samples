import json
from os import path

filename = ".amphora.cache.json"

def load() -> dict():
    if path.exists(filename):
        f = open(filename, "r")
        j = f.read()
        return json.loads(j)
    else:
        return {}

def save(cache):
    j = json.dumps(cache)
    f = open(filename, "w")
    f.write(j)