import os
from datetime import datetime, timedelta
import pytz
import constants
from amphora.client import AmphoraDataRepositoryClient, Credentials
from amphora_api_client import DateTimeRange
from pandas import DataFrame

# login
username = os.getenv('username')
password = os.getenv('password')
credentials = Credentials(username, password)
client = AmphoraDataRepositoryClient(credentials)

insights = client.get_amphora(constants.insights_id)

# save alert method
def alert(name: str, text: str):
    # create the file locally
    filepath = f'{name}.txt'
    file_object = open(filepath, "w+")
    file_object.write(text)
    file_object.flush()
    file_object.close()
    insights.push_file(filepath, f'{name}')
    print(f'Uploaded file {name}')


def check_max_and_alert(df: DataFrame, key: str, threshold: int, file_prefix: str, message: str):
    series = df[key]
    maximum = series.max()
    print(f'Maximum: {maximum}')
    if(maximum > threshold):
        print(f"ALERT, high value recorded: ({maximum})")
        points = df.loc[df[key] == maximum]
        mean_time = points.index.mean()
        mean_time_local = mean_time.astimezone(
            pytz.timezone('Australia/Melbourne'))
        alert(f'{file_prefix}_{mean_time_local.date()}',
              f'{message}\nValue was {maximum} at approximately {mean_time_local}')


def check_min_and_alert(df: DataFrame, key: str, threshold: int, file_prefix: str, message: str):
    series = df[key]
    minimum = series.min()
    print(f'Minimum: {minimum}')
    if(minimum < threshold):
        print(f"ALERT, low value recorded: ({minimum})")
        points = df.loc[df[key] == minimum]
        mean_time = points.index.mean()
        mean_time_local = mean_time.astimezone(
            pytz.timezone('Australia/Melbourne'))
        alert(f'{file_prefix}_{mean_time_local.date()}',
              f'{message}\nValue was {minimum} at approximately {mean_time_local}')


# set up the date ranges we care about
forecast_range = DateTimeRange(
    _from=datetime.utcnow() + timedelta(hours=-1), to=datetime.utcnow() + timedelta(days=1))
observations_range = DateTimeRange(
    _from=datetime.utcnow() + timedelta(days=-1), to=datetime.utcnow())

# get the data
weather_forecast = client.get_amphora(constants.weather_forecasts_id)
weather_forecast_df = weather_forecast.get_signals().pull(
    date_time_range=forecast_range, include_wt=True, tsi_api="GetEvents").to_pandas()
print('Describe forecasts')
print(weather_forecast_df.describe())

weather_observations = client.get_amphora(constants.weather_observation_id)
weather_observations_df = weather_observations.get_signals().pull(
    date_time_range=observations_range, include_wt=True, tsi_api="GetEvents").to_pandas()
print('Describe observations')
print(weather_observations_df.describe())

# select series
temperature_forecast = weather_forecast_df['temperature']
temperature_observations = weather_observations_df['airTemp']

# MAXIMAS
# forecast maxima
check_max_and_alert(weather_forecast_df, 'temperature', constants.max_temperature_threshold,
                    'high_temp_forecast', 'A high temperature as been forecast.')

# observation maxima
check_max_and_alert(weather_observations_df, 'airTemp', constants.max_temperature_threshold,
                    'high_temp_observed', 'A high temperature as been observed.')

# MINIMAS
check_min_and_alert(weather_forecast_df, 'temperature', constants.min_temperature_threshold,
                    'low_temp_forecast', 'A low temperature as been forecast.')

# observation maxima
check_min_and_alert(weather_observations_df, 'airTemp', constants.min_temperature_threshold,
                    'low_temp_observed', 'A low temperature as been observed.')
