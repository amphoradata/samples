# Import Amphora modules
from amphora.client import AmphoraDataRepositoryClient, Credentials

# Import non-Amphora modules
import os

# Login to amphoradata.com
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password')) 
client = AmphoraDataRepositoryClient(credentials)

# Set metadata for Amphora
name = "Amphora_Name" #Name the amphora as string
description = "Amphora_Description" #Describe the amphora as string
price = 0 #Monthly price as float
labels = ["Label_1","Label_2","Label_3"]  #List of 2-5 one word strings
lat = 0.0 #Enter latitude as float
lon = 0.0 #Enter longitude as float

# Create Amphora
amphora = client.create_amphora(name=name, description=description, labels=labels, price=price, lat=lat, lon = lon)
