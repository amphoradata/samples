# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 17:48:07 2020
@author: Isaac
"""

# Import Amphora librarys
from amphora.client import AmphoraDataRepositoryClient, Credentials

# Import non-Amphora librarys
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Login to amphoradata.com
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password')) 
client = AmphoraDataRepositoryClient(credentials)

# Get Amphora of interest
f=open("Amphora_id.txt", "r")
amphora_id = f.read()

# Set time points of interest
start = datetime.utcnow() + timedelta(hours=-48)
end = datetime.utcnow()
dt_range = DateTimeRange(_from=start, to=end)

# Pull data from Amphora
amphora = client.get_amphora(amphora_id)
signals = amphora.get_signals()
df = signals.pull(date_time_range=dt_range).to_pandas(t_as_index=False)

# Make plot of data
df.plot(x ='t', y='timeProduct')
plt.show()	
