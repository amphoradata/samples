# Import Amphora librarys
from amphora.client import AmphoraDataRepositoryClient, Credentials
import amphora_api_client as a10a
from amphora_api_client.rest import ApiException
from amphora_api_client.configuration import Configuration

# Import non-Amphora librarys
from array import array 
import os
import numpy as np
import time
from datetime import datetime, timedelta


# Login to amphoradata.com
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password')) 
client = AmphoraDataRepositoryClient(credentials)
amphora_api = a10a.AmphoraeApi(client.apiClient)
