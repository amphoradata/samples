import os
import getpass
from amphora.client import AmphoraDataRepositoryClient, Credentials
from amphora_api_client import ApplicationsApi, CreateApplication, AppLocation, UpdateApplication

username = input("Enter your Amphora username:")
password = getpass.getpass()
# password = input("Password:")

credentials = Credentials(username=username, password=password)
client = AmphoraDataRepositoryClient(credentials)

# create an application API to interact
appApi = ApplicationsApi(client.apiClient)

app_name = input("Enter a name for your app (default: my_app):") or "my_app"
logout_url = input(
    "Enter a logout callback URL (default: http://localhost:3000/logout):") or "http://localhost:3000/logout"

# add the default location
appLocations = [
    AppLocation(origin="http://localhost:3000",
                allowed_redirect_paths=["/#/callback"])
]

# actually these are added as extras
origin = input(
    "Enter the deployed URL for your app (default: http://localhost:3000):") or None
redirect_path = input(
    "Enter an allowed redirect path (default: /#/callback):") or None

create_app = CreateApplication(
    name=app_name,
    locations=appLocations,
    logout_url=logout_url)

if(origin is not None and redirect_path is not None):
    appLocations.append(
        AppLocation(origin=origin, allowed_redirect_paths=[redirect_path])
    )

input(
    f'You are about to register an app named {create_app.name}. Press any key to continue, or ctrl+c to cancel...')

app = appApi.applications_create_application(create_app)
print(f'Your Application ID is {app.id}')
