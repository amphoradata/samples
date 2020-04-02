# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import os
from datetime import datetime, timedelta

from amphora.client import AmphoraDataRepositoryClient, Credentials
import amphora_api_client as a10a
from amphora_api_client.rest import ApiException
from amphora_api_client.configuration import Configuration
import csv
import urllib.request
import ast

country_codes = ["AUS","NZL","PNG","GBR","CAN","USA","CHN","FJI","IDN","IND"]
country_id_stor = []

# Set up connection to amphoradata.com
# provide your login credentials
credentials = Credentials(username=os.getenv('username'), password=os.getenv('password'))
# create a client for interacting with the public Amphora Data Repository
client = AmphoraDataRepositoryClient(credentials)

date_str = []

def importCsv(file):
    cnt = 0
    with open(file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data:
            if row:
                date_str.append(row)
                cnt += 1
        print(cnt)

importCsv("dates_of_interest.csv")


def get_country_covid_data(country):
    sep=''
    ## Get data
    with urllib.request.urlopen(sep.join(["https://wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai/jhu-edu/timeseries?iso3=",country,"&onlyCountries=true"])) as response:
       covid_bytes = response.read()
       covid_decode = covid_bytes.decode("utf-8")
       covid_interim = ast.literal_eval(covid_decode)
       covid_data = covid_interim[0]
       covid_time_series = covid_data["timeseries"]
       T = len(covid_time_series)
       country_name = covid_data["countryregion"]
       location = covid_data["location"]
       time_for_signal = []
       confirmed_num = []
       active_num = []
       deaths_num = []
       recovered_num = []
       signalsCC=[]
       signalsRC=[]
       signalsDT=[]
       signalsAC=[]
       
       for t in range(T):
           try:
               date_of_interest = date_str[t][0]
               data_for_day = covid_time_series[date_of_interest]
               print(date_of_interest)
               
               time_for_signal = datetime.strptime(date_str[t][1], "%d/%m/%Y")
               confirmed_num = data_for_day["confirmed"]
               deaths_num = data_for_day["deaths"]
               recovered_num = data_for_day["recovered"]
               active_num = data_for_day["confirmed"]-data_for_day["deaths"]-data_for_day["recovered"]
               
               signalsCC.append(dict(t = time_for_signal, confirmedCases = confirmed_num))
               signalsRC.append(dict(t = time_for_signal, recoveredCases = recovered_num))
               signalsDT.append(dict(t = time_for_signal, deaths = deaths_num))
               signalsAC.append(dict(t = time_for_signal, activeCases = active_num))
           except:
               print(t) 
    
for country in country_codes:
    get_country_covid_data(country)    
        

