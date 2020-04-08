# Import Amphora modules
from amphora.client import AmphoraDataRepositoryClient, Credentials

# Import non-Amphora modules
import os

# Login to amphoradata.com
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password')) 
client = AmphoraDataRepositoryClient(credentials)

# Create signal object. Update as often as you wish
Signals = [dict(t = datetime_value, signal_name = signal_value)] 

# Get Amphora object
amphora = client.get_amphora(Amphora_id) 

# Create update signal
amphora.push_signals_dict_array(Signals) 
