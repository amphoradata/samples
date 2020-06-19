# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:47:16 2020

@author: Isaac
"""
# Import amphora modules
from amphora.client import AmphoraDataRepositoryClient, Credentials

# Import non-amphora modules
import time
import mlflow
import os
from datetime import datetime, timedelta

## Set up log metrics
start = time.time()
sep='_'
experimentId = 0
mlflow.set_tracking_uri("your_mlflow_address")
runName = sep.join(['Job_at',str(datetime.utcnow())])
#mlflow.start_run(experiment_id=experimentId, run_name =runName)
mlflow.log_metric("time_to_complete", 0)
mlflow.log_metric("amphoras_uploaded",0)
mlflow.log_metric("run_complete",0)

# Set up connection to amphoradata.com
credentials = Credentials(username=os.getenv(username), password=os.getenv(password))
client = AmphoraDataRepositoryClient(credentials)

cnt=0
for i in range(Some_number):

  # Get the amphora you want to push data to
  amphora = client.get_amphora(Amphora_id) 

  # Connect to original data source
  # Add code/module as needed

  # Do analytics/transforms on data
  # Add code/module as needed

  # Push to Amphora
  # Add code as needed
  amphora.push_signals_dict_array(Signals) 
  amphora.push_file(file_path)

  # Update loggers in loop
  cnt=cnt+1
  mlflow.log_metric("amphoras_uploaded",cnt)

# Close out mlflow tracking
end = time.time()
mlflow.log_metric("time_to_complete", end - start) 
mlflow.log_metric("run_complete",1)
mlflow.end_run()     

# Finish job
print('Job is finished')
