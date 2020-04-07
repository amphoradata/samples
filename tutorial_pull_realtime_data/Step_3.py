# Import Amphora librarys
from amphora.client import AmphoraDataRepositoryClient, Credentials

# Import non-Amphora librarys
import os

# Login to amphoradata.com
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password')) 
client = AmphoraDataRepositoryClient(credentials)
