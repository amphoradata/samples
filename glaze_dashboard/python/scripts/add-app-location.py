import os
import getpass
from amphora.client import AmphoraDataRepositoryClient, Credentials
from amphora_api_client import ApplicationsApi, CreateApplication, AppLocation, UpdateApplication

username = input("Enter your Amphora username:")
password = getpass.getpass()

credentials = Credentials(username=username, password=password)
client = AmphoraDataRepositoryClient(credentials)

# create an application API to interact
appApi = ApplicationsApi(client.apiClient)
appId = input("Enter your Amphora application Id:")
origin = input("Enter your deployed host/ CORS origin:")
redirect_path = input(
    "Enter the redirect path (default: /#/callback):") or "/#/callback"

new_location = AppLocation(origin=origin, allowed_redirect_paths=[redirect_path])

application = appApi.applications_read_application(appId)
print(f'Found existing application: {application.name}')
locations = application.locations
locations.append(new_location)

update = UpdateApplication(
    name=application.name, logout_url=application.logout_url, id=application.id, locations=locations)
appApi.applications_update_application(appId, update)
print('updated application')