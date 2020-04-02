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

## Choose the country

## Log in to Amphora
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password'))
# create a client for interacting with the public Amphora Data Repository
client = AmphoraDataRepositoryClient(credentials)
amphora_api = a10a.AmphoraeApi(client.apiClient)

date_str=[]
def importCsv(file):
    cnt = 0
    with open(file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data:
            if row:
                date_str.append(row)
                cnt += 1
        print(cnt)

def flatten_time_series_data(time_series_data):
    unique_dt = Counter(time_series_data.timestamps).keys()     # Get unique time stamps
    num_dt = len(unique_dt)                                     # Get number of unique time stamps
    num_prop = len(time_series_data.properties)                 # Get number of properties
    
    data_name = []
    data_array = np.zeros((num_prop-1,num_dt))
    for i in range(1,num_prop):           # Get values for property i
        data_name.append(time_series_data.properties[i].name)   # Get name for property i
        non_none_indicies = [j for j, val in enumerate(time_series_data.properties[i].values) if val != None]                 #location of that data
        for t in range(num_dt):
            element_of_interest = non_none_indicies[t]
            data_array[i-1][t] = time_series_data.properties[i].values[element_of_interest]
        
   
    return data_array, unique_dt, data_name      


importCsv("dates_of_interest.csv")

amphora_id = 'fca8998a-2d0e-4afa-a9aa-1467759a8d9a'

T=60


## Get the data
ts_api = a10a.TimeSeriesApi(client.apiClient)
time_range = a10a.DateTimeRange(_from = datetime.utcnow() + timedelta(days=-T) , to= datetime.utcnow())
variables = {"confirmedCases": a10a.NumericVariable( kind="numeric", value=a10a.Tsx(tsx="$event.confirmedCases"), aggregation=a10a.Tsx(tsx = "it doesn't matter")),
             "activeCases": a10a.NumericVariable( kind="numeric", value=a10a.Tsx(tsx="$event.activeCases"), aggregation=a10a.Tsx(tsx = "it doesn't matter")),
             "recoveredCases": a10a.NumericVariable( kind="numeric", value=a10a.Tsx(tsx="$event.recoveredCases"), aggregation=a10a.Tsx(tsx = "it doesn't matter")),
             "deaths": a10a.NumericVariable( kind="numeric", value=a10a.Tsx(tsx="$event.deaths"), aggregation=a10a.Tsx(tsx = "it doesn't matter"))}

get_series_query = a10a.GetSeries([amphora_id], search_span= time_range, inline_variables= variables) # the complete query
time_series_data = ts_api.time_series_query_time_series( a10a.QueryRequest(get_series= get_series_query))


S0 = 1352640000 #country population

data_array, unique_dt, data_name  = flatten_time_series_data(time_series_data)
print(data_name)
for i in range(4):
    if data_name[i] == 'activeCases':
        I = data_array[i]
    elif data_name[i] == 'recoveredCases':
        R = data_array[i]    
    elif data_name[i] == 'deaths':
        D = data_array[i]    
        
print(I)
print(R)
print(D)
S = np.zeros(len(I))
      
        
for t in range(len(I)):
    print(t)
    S[t] = S0-I[t]-R[t]-D[t]

## Compute the derivatives
# take a 3 day moving average
mov_av = 7
dSdt = np.zeros(T)
dIdt = np.zeros(T)
dRdt = np.zeros(T)
dDdt = np.zeros(T)
dSdt_raw = np.zeros(T)
dIdt_raw = np.zeros(T)
dRdt_raw = np.zeros(T)
dDdt_raw = np.zeros(T)

for t in range(1,T-2):
    dSdt_raw[t] = (S[t]-S[t-1])/S[t-1]
    if I[t-1] >0:
        dIdt_raw[t] = (I[t]-I[t-1])/I[t-1]
    else: 
        dIdt_raw[t] = I[t]
    if R[t-1] >0:
        dRdt_raw[t] = (R[t]-R[t-1])/R[t-1]
    else: 
        dRdt_raw[t] = R[t]
    if D[t-1] >0:
        dDdt_raw[t] = (D[t]-D[t-1])/D[t-1]
    else: 
        dDdt_raw[t] = D[t]
    if t>mov_av:
        dSdt[t] = np.mean(dSdt_raw[t-mov_av+1:t])
        dIdt[t] = np.mean(dIdt_raw[t-mov_av+1:t])
        dRdt[t] = np.mean(dRdt_raw[t-mov_av+1:t])
        dDdt[t] = np.mean(dDdt_raw[t-mov_av+1:t])
        

## Compute the parameters
alpha = np.zeros(T-2)
beta = np.zeros(T-2)
gamma = np.zeros(T-2)
signals = []

for t in range(1+mov_av,T-2):
    if I[t] != 0:
        beta[t] = - dSdt[t]*10**15 
        beta[t] = beta[t] / S[t] / I[t]
        alpha[t] = dRdt[t] / I[t] *100
        gamma[t] = dDdt[t] / I[t] *100
    else: 
        beta[t]=0
        alpha[t]=0
        gamma[t]=0
    time_for_signal = time_series_data.timestamps[t]
    signals.append(dict(t = time_for_signal, beta = beta[t], alpha = alpha[t], gamma = gamma[t]))

## Plot results
plt.figure(figsize=(20,10))
plt.subplot(231)
plt.plot(I[-28:-1])
plt.title('Total infections (#)')
plt.subplot(232)
plt.plot(R[-28:-1])
plt.title('Total recovered (#)')
plt.subplot(233)
plt.plot(D[-28:-1])
plt.title('Total deaths (#)')        
plt.subplot(234)      
plt.plot(beta[-28:-1])
plt.title('Infection rate beta (%*10^13)')
plt.subplot(235)
plt.plot(alpha[-28:-1])
plt.title('Recovery rate alpha (%)')
plt.subplot(236)
plt.plot(gamma[-28:-1] )
plt.title('Death rate gamma (%)')
plt.show()
