# Import Amphora modules
from amphora.client import AmphoraDataRepositoryClient, Credentials

# Import non-Amphora modules
import os

# Login to amphoradata.com
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password')) 
client = AmphoraDataRepositoryClient(credentials)

# Get Amphora object
amphora = client.get_amphora(Amphora_id) 

# Pull file
amphora.get_file(file_name).pull(destination_file_path)
