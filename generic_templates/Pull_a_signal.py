# Import Amphora modules
from amphora.client import AmphoraDataRepositoryClient, Credentials

# Import non-Amphora modules
import os

# Login to amphoradata.com
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password')) 
client = AmphoraDataRepositoryClient(credentials)

# Get Amphora object
amphora = client.get_amphora(Amphora_id) 

# Pull signal
signals = amphora.get_signals()

# Convert signal to Pandas dataframe
df = signals.pull().to_pandas()

# Alternate: convert signal from specific  time to Pandas dataframe
from amphora_api_client import DateTimeRange
time_range = DateTimeRange(_from=start_time, to=end_time)
df = signals.pull(date_time_range=time_range).to_pandas()
