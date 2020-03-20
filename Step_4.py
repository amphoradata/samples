# Import Amphora librarys
import amphora_client as a10a
from amphora_client.configuration import Configuration
from amphora_extensions.file_uploader import FileUploader

# Import non-Amphora librarys
from array import array 
import os
import numpy as np
import time
from datetime import datetime, timedelta


# Login to amphoradata.com
configuration = Configuration()
configuration.host = "https://app.amphoradata.com"
auth_api = a10a.AuthenticationApi(a10a.ApiClient(configuration))
token_request = a10a.TokenRequest(username=os.getenv('username'), password=os.getenv('password'))
res = auth_api.authentication_request_token(token_request = token_request )
configuration.api_key["Authorization"] = "Bearer " + res
amphora_api = a10a.AmphoraeApi(a10a.ApiClient(configuration))

# Define model function
def time_product(date_time):
  time_hour = date_time.hour
  time_minute = date_time.minute
  time_second = date_time.second

  time_prod = time_hour * time_minute * time_second
  
  return time_prod

#####################################

# Run model
time_now = date_time.utcnow()
time_prod = time_product(time_now)

# Create Amphora
# Define metadata for Amphora
sep=" "
amphora_description = "This is an Amphora for a tutorial on how to make Amphoras"
amphora_tnc = "Creative_Commons_4p0"
amphora_name = "Tutorial: How to make and upload an Amphora"
amphora_labels = "tutorial,timeseries"
amphora_price = 10   # Monthly price of Amphora
amphora_lat = -27.45714
amphora_lon = 153.07106

## Create an Amphora 
dto = a10a.CreateAmphora(name = amphora_name, lat = amphora_lat, lon = amphora_lon, 
                         price = amphora_price, description = amphora_description, 
                         terms_and_conditions_id = amphora_tnc, labels = amphora_labels)
new_amphora = amphora_api.amphorae_create(create_amphora=dto)

# Save Amphora ID for later
File_object = open("Amphora_id.txt","w") 
File_object.write(new_amphora.id)
File_object.close()

# Now create signal 
yourSignal=a10a.Signal(_property = "timeProduct", value_type = "Numeric", 
                       attributes = {"units": "HMS"})
amphora_api.amphorae_signals_create_signal(new_amphora.id, signal = yourSignal)
signalStore=[]
signalStore.append({"t": time_now, "timeProduct": time_prod})

# Push signal
amphora_api.amphorae_signals_upload_signal_batch(new_amphora.id, signalStore)
