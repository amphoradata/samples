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

# Get existing Amphora ID
File_object = open("Amphora_id.txt","r") 
Amphora_id = File_object.read()
File_object.close()


# Define model function
def time_product(date_time_obj):
  time_hour = date_time_obj.hour
  time_minute = date_time_obj.minute
  time_second = date_time_obj.second

  time_prod = time_hour * time_minute * time_second
  
  return time_prod

#####################################

# Run model
time_now = datetime.utcnow()
time_prod = time_product(time_now)

# Now create signal 
signalStore=[]
signalStore.append({"t": time_now, "timeProduct": time_prod})

# Push signal
amphora_api.amphorae_signals_upload_signal_batch(Amphora_id, signalStore)
