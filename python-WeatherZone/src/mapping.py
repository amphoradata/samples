import pickle
from os import path

filename = "cache.p"
# maps WeatherZone location code to an Amphora Id
def wz_locations():
    return {
        '13388': "8f295e38-02c9-489f-b272-304cdcef53ed", # Berri, SA
        '4205': "57d6593f-1889-410a-b1fb-631b6f9c9c85", # Albury NSW
        '9396': "6c6bec6a-b672-43f6-a624-2e32186e68cd" # Spring Hill, Brisbane, QLD
        }

# locations should be a dictionary wzId -> amphoraId
def wz_save(locations):
    #locations.update(wz_locations())
    pickle.dump( locations, open( filename, "wb" ) )

def wz_load():
    if path.exists(filename):
        locations = pickle.load( open( filename, "rb" ) )
        locations.update(wz_locations())
        return locations
    else:
        return wz_locations()
