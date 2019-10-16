#!/bin/bash
echo Deploying Resources to Azure
set -e
rg=amphora-nem-${RANDOM:0:2}
location=australiaeast
func=nemfunc${RANDOM:0:2}

host=https://beta.amphoradata.com
user=CHANGE_ME
pass=CHANGE_ME

az group create -l $location -n $rg --tags project=samples

storage=funcstore${RANDOM:0:2}
az storage account create -n $storage -l $location -g $rg --sku Standard_LRS

az functionapp create -n $func --storage-account $storage --os-type Linux -c $location --runtime dotnet -g $rg

az functionapp config appsettings set -n $func -g $rg --settings "Amphora__Host=$host" "Amphora__UserName=$user" "Amphora__Password=$pass"

echo "Waiting for function app..."
sleep 20

echo Deploying Function App
func azure functionapp publish $func
