import pickle
from os import path

filename = "cache.p"

# locations should be a dictionary wzId -> amphoraId
def wz_save(locations):
    #locations.update(wz_locations())
    pickle.dump( locations, open( filename, "wb" ) )

def wz_load():
    if path.exists(filename):
        locations = pickle.load( open( filename, "rb" ) )
        return locations
    else:
        return {}
