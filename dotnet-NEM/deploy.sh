#!/bin/bash

rg=amphora-nem-${RANDOM:0:2}
location=australiaeast
func=nemfunc${RANDOM:0:2}

host=
user=
pass=

az group create -l $location -n $rg

storage=funcstore${RANDOM:0:2}
az storage account create -n $storage -l $location -g $rg --sku Standard_LRS

az functionapp create -n $func --storage-account $storage  --consumption-plan-location $location --runtime dotnet -g $rg

az functionapp config appsettings set -n $func -g $rg --settings "Amphora__Host=$host" "Amphora__UserName=$user" "Amphora__Password=$pass"

az functionapp deployment source config --repo-url https://github.com/amphoradata/samples --app-working-dir dotnet-NEM

