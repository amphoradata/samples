# Import Amphora modules
from amphora.client import AmphoraDataRepositoryClient, Credentials

# Import non-Amphora modules
import os

# Login to amphoradata.com
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password')) 
client = AmphoraDataRepositoryClient(credentials)

# Set metadata for Amphora
name = #Name the amphora as string
description = #Describe the amphora as string
price = #Monthly price as float
labels = ["Label_1","Label_2","Label_3"]
lat = #Enter latitude as float
lon = #Enter longitude as float

# Create Amphora
amphora = client.create_amphora(name=name, description=desc, labels=labels, price=price, lat=lat, lon = lon)
