# WeatherZone API Sample

This sample shows you how to *Load* data from an external web API (in this case the WeatherZone API), *Transform* into an Amphora supported format, and *Load* into an Amphora for use on the Amphora Data platform.

## Prerequisites

* Have an Amphora Data account.
* Have Python or Docker installed.

# Quickstart

## Create an Amphora.

Create an Amphora to hold your data. Make sure to give the Amphora a meaningful name, description, and location, so that consumers of the data know what they are getting.

> Navigate to `Amphorae` in the Nav Bar, and click the blue `Create` button.

## Add Signal Properties to your Amphora.

We're going to be tracking the numeric temperature and rain probability forecasts, as well as the description of the weather and the time the prediction was loaded from WeatherZone. To do this we need to add these as *Properties* to our Amphora, so the platform knows what data to expect (and what to reject!)

> Click `Signals` in the Amphora details page, and then click the `+` button to add a Property.

We're going to add the following properties:

| Property Name   | Property Type | Weatherzone Property Name |
|-----------------|---------------|---------------------------|
| temperature     | numeric       | temperature               |
| rain_prob       | numeric       | rain_prob                 |
| prediction_time | string        | -                         |
| description     | string        | icon_phrase               |

You don't need to explicity add the `t` property (the timestamp property). This is included by default on every signal, and defaults to the current UTC time. 

## Copy the Id of the Amphora

Now we've created an Amphora for our weather data, we can run the scripts in this repository. First, however, you'll need to replace the Amphora Id in [the environment file](.env) with the Id of the Amphora you just created. You can find the Id in your browsers navigation bar.

> Copy the Amphora Id from the browsers navigation bar

## Check your environment variables

[The environment file](.env) contains configuration information. You'll need to set the following:

wz_user -> Your WeatherZone API username. If you don't have one, you can leave this blank and change the code to pull from the github gist.
wz_password -> WeatherZone API password. See note above.
wz_lc -> WeatherZone location code.
username -> Amphora Data username
password -> Amphora Data password. Keep this secret!
host -> Amphora Data host. Probably `https://beta.amphoradata.com`
amphora_id -> the Id you copied in the step above.

## Run the code.

### Using docker compose

```sh
docker-compose run index
```

### Using Python

```sh
pip install -r requirements.txt
python index.py
```

## View the Signals

You should now be able to view the weather data on the Amphora Data website. Note that it may take up to a minute for the signal data to become available.

