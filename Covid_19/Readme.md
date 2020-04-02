### H3 This sample shows you how to do real time modelling of Covid-19.

In this sample we will use up-to-date reported Covid numbers from 10 countries. We will use a standard disease model, the SIR model, to classify Covid numbers and estimate model parameters.

This approach is more interesting than looking at raw numbers as we can analyse and compare infectious, recovery, and death rates by country and by time. With this we can see if a countries quarantine is helping to decrease the infectious rate, if a countries death rate is higher than another, and similar questions.

#### H4 Step 1: Get the raw data
We are getting our data from John Hopkins. We use a simple API query to pull data for countries that we are interested in
``` "https://wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai/jhu-edu/timeseries?iso3=",country,"&onlyCountries=true" ```

We can then get the timeseries that we want by
```
confirmed_num = data_for_day["confirmed"]
deaths_num = data_for_day["deaths"]
recovered_num = data_for_day["recovered"]
active_num = data_for_day["confirmed"]-data_for_day["deaths"]-data_for_day["recovered"]
``` 
where
```data_for_day```
is the data for that country for a given day.

#### H4 Step 2: Create the individual country Amphoras and push signals
We can now simply create each countries Amphora for their Covid numbers with
```
amphora_description=sep.join(["Covid 19 data for ", country_name ,"\n Properties include: \n- Number of confirmed cases \n - Number of recovered cases \n - Number of deaths \n - Number of active cases  \n Data obtained from John Hopkins Institute"])
amphora_tnc="Creative_Commons_0"
amphora_name=sep.join(["Covid 19 data for ",country_name])
labels=['Covid, actuals, timeseries']
amphora = client.create_amphora(name = amphora_name, lat = location["lat"], lon = location["lng"], price = 0, description = amphora_description, terms_and_conditions_id = amphora_tnc, labels=labels)
country_id_stor.append([country,amphora.amphora_id])
```

We can then create the different signals as
``` amphora.create_signal("confirmedCases", attributes={"units":"No"}) ```
then push the appropriate signal with
``` amphora.push_signals_dict_array(signals)``` 

#### H4 Step 3: Estimate SIR model parameters
For our model, we will use a Susceptible (S)-Infected (I)-Recovered (R)-Dead (D) model. This compartmentalises all of a population into four types and defines the transition rates between each compartment. Formally the model is defined as a set of differential equations
```dS[t]/dt = - beta * S[t] * I[t]
dI[t]/dt = beta * S[t] * I[t] - alpha * I[t] - gamma * I[t]
dR[t]/dt = alpha * I[t]
dD[t]/dt = gamma * I[t]
```

As we don't have the derivatives, we need to compute them from the data that we have. We use
```
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
```
Note we use a 7 day moving average to get our derivatives rather than the day difference. This is because numbers in most countries are still quite small and fluctuate like a Poisson distribution. 

Assuming our parameters change over time and solving for our parameters gives us
```beta[t] = - dS[t]/dt / (S[t] * I[t])
alpha[t] = dR[t]/dt / I[t]
gamma[t] = dD[t]/dt / I[t]
```


#### H4 Step 4: Compare parameters
