# DotNet ETL with Azure Functions

This sample shows you how to run a periodic ETL job in C# using the [Amphora Data DotNet SDK](https://github.com/amphoradata/dotnet-sdk), and [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-overview).

# How it works

This directory contains the source code for an Azure Function written in C#. The entrypoint for this function is [ETL_NEM](ETL_NEM.cs).
In this file, you can see the the following constructor, which defined the period we want to run this function, which is triggered by a timer. In this case, the timer will trigger the function every 6 hours.

```cs
public static async Task Run([TimerTrigger("0 */6 * * *")] TimerInfo myTimer, 
    ILogger log, 
    ExecutionContext context)
{
    
}
```

The grunt of the work in done by the [Engine](Engine.cs) class, where the NEM data is *extracted*,  *transformed* and *loaded* into Amphorae.

In order to keep data in reasonable sized units, we using a [Mapping](Mapping.cs) class, so that different NEM regions will be mapped to different Amphora (i.e. South Australian eletricity data will be in 1 amphora, NSW in another, etc.)

# How to run

## Requirements

* [DotNet CLI](https://docs.microsoft.com/en-us/dotnet/core/tools/?tabs=netcore2x)
* [The Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
* [Azure Functions CLI](https://github.com/Azure/azure-functions-core-tools#installing)
* An Azure account
* An Amphora Data account

## Configure the application

### Set your username and password

The [deploy.sh](deploy.sh) script does all the work for you to deploy the app. However, you need to enter your Amphora Data username and password in that script.

### Create some Amphorae to hold the data

In the Amphora Data web application, create new Amphora for each NEM state, as shown in this table:

| NEM Region | State           |
|------------|-----------------|
| Sa1        | South Australia |
| Nsw1       | New South Wales |
| Qld1       | Queensland      |
| Tas1       | Tasmania        |
| Vic1       | Victoria        |

### Copy the Ids into Mapping.cs

Copy the Ids of each of the amphora you made above, into their respective place in [Mapping.cs](Mapping.cs). This is how the code knows where to put the data. You can find the Id of the Amphora in the URL. Alternatively, if you have lot's of Amphora, it is possible to create them via the SDK.

Alternatively, you can put all the data into 1 Amphora. Just duplicate the Ids in [Mapping.cs](Mapping.cs), and complete the following steps for just 1 amphora.

### Set up the Amphora Signal properties 

Each Amphora will contain data relating to the price and volume of electricity in each region. We'll need to tell the Amphora which properties to expect. Click on each Amphora, and again click on `Signals` in the top right. Now click the `+` button to add properties as shown in the table below. Do this for each Amphora.

| Property Name       | Property Type |
|---------------------|---------------|
| price               | Numeric       |
| scheduledGeneration | Numeric       |
| periodType          | String        |


## Deploy the Function App

Simply run `deploy.sh` to deploy the web app. This script depends on having the Azure CLI and Functions CLI installed.

The script will create a new resource group, storage account, and function app. The function app will run there every 6 hours.

## View the data in Amphora Data

You should now be seeing data live in Amphora Data. It's now ready to be shared with others or consumed elsewhere.

