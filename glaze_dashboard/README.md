# Glaze Tutorial: Sample Dashboard

In this tutorial, we're going to build a data driven dashboard, fron scratch, using [Amphora Glaze](https://www.amphoradata.com/glaze/).

> This tutorial requires a subscription to Amphora `Glaze`. 

> If you aren't registed, head to [the app](https://app.amphoradata.com/) to register.

## Clone this Repository

To begin, clone this repo, and open this directory:

```sh
git clone https://github.com/amphoradata/samples.git
cd samples/glaze_dashboard
```

## Create an Amphora Application

Amphora Applications allow you to connect external apps to Amphora Data services. It enables OAuth logins to your app with the Amphora Identity system, and it allows the Amphora backend to response (via CORS) to requests from the app.

### Creating the application

We are going to need the Amphora Data python SDK installed.

#### Install the Python SDK

In a terminal:

```sh
cd python
pip install -r requirements.txt
```

#### Run the create-application.py script

[This helpful script](python/scripts/create-application.py) enables you to create a new Amphora application.

```sh
> python create-application.py

Enter your Amphora username:rian@amphoradata.com
Password:
https://app.amphoradata.com
Enter a name for your app (default: my_app):sample_glaze_dashboard
Enter a logout callback URL (default: http://localhost:3000/logout):
Enter the deployed URL for your app (default: http://localhost:3000):
Enter an allowed redirect path (default: /#/callback):
You are about to register an app named sample_glaze_dashboard. Press any key to continue, or ctrl+c to cancel...
Your Application ID is f48fed4f-569e-4524-8432-b5ae4444eca4   # <-- copy this id
```


## Creating a react app

For this dashboard, we're going to use [react-amphora](https://github.com/xtellurian/react-amphora), a frontend react library that removes a lot of boilerplate code.