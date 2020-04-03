
"""
Created on Thu Apr  2 13:19:28 2020

@author: Isaac
"""

## Import packages
import time
import os
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from amphora.client import AmphoraDataRepositoryClient, Credentials
import amphora_api_client as a10a
from amphora_api_client.rest import ApiException
from amphora_api_client.configuration import Configuration
import csv
  
## Log in to Amphora
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password'))
# create a client for interacting with the public Amphora Data Repository
client = AmphoraDataRepositoryClient(credentials)
amphora_api = a10a.AmphoraeApi(client.apiClient)

importCsv("country_index.csv")


parameters = ["beta"]

## Create Amphora for beta
amphora_description="Beta parameter data for Covid 19 for Australia, New Zealand, Great Britain, Canada, USA, China, Indonesia and India. \n beta is from SIRD model \n dS/dt = - beta * S * I \n dI/dt = beta * S * I - alpha * I - gamma * I \n dR/dt = alpha * I \n dD/dt = gamma * I"
amphora_tnc="Creative_Commons_0"
amphora_name="Beta parameter for 8 countries"
labels=['Covid, actuals, timeseries']

## Create an Amphora 
amphora = client.create_amphora(name = amphora_name, price = 0, description = amphora_description, terms_and_conditions_id = amphora_tnc, labels=labels)
amphora_id = amphora.amphora_id
amphora_api = a10a.AmphoraeApi(client.apiClient)
T=25
for i in range(len(country_stor)):
    sep=""
    # Pull beta signal
    ## Get the data
    ts_api = a10a.TimeSeriesApi(client.apiClient)
    time_range = a10a.DateTimeRange(_from = datetime.utcnow() + timedelta(days=-T) , to= datetime.utcnow()+ timedelta(days=-5))
    variables = {"beta": a10a.NumericVariable( kind="numeric", value=a10a.Tsx(tsx="$event.beta"), aggregation=a10a.Tsx(tsx = "it doesn't matter"))}
    
    get_series_query = a10a.GetSeries([country_stor[i][0]], search_span= time_range, inline_variables= variables) # the complete query
    time_series_data = ts_api.time_series_query_time_series( a10a.QueryRequest(get_series= get_series_query))
    
    data_array, unique_dt, data_name  = flatten_time_series_data(time_series_data)
    unique_dt_list = list(unique_dt)
    beta = data_array[0]
    
    # scale rate for comparison
    scalar_multiple = float(country_stor[i][2]) / (10**15)
    beta_scaled = beta * scalar_multiple
    
    # Push beta signal
    signals = []
    betaCountry = sep.join(['beta',country_stor[i][1]])
    amphora.create_signal(betaCountry, attributes={"units":"Rate"})
    for t in range(len(unique_dt_list)):
        time_for_signal = unique_dt_list[t]
        signals.append(dict({"t": time_for_signal, "%s"%betaCountry: beta_scaled[t]}))
    amphora.push_signals_dict_array(signals)

