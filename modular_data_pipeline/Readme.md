# Modular data pipelines improve reusability and reliability for ETL and analytics

Pipelines route data from a source to a destination. All analytics and extract-transfer-load (ETL) involve them. Pipelines come in all shapes and sizes but modular pipelines can be best if you are working collaboratively, without too much legacy tech, and have a big backlog of similar but different data and analytics tasks.

This readme is a companion to a video and all code is in this GitHub repo.

## What exactly is a modular data pipeline?

A modular data pipeline (MDP) is a process to move or transform data that is broken down into the smallest steps possible. Each of these steps is a very small data pipeline component that, when added together, form a larger data pipeline. Essentially it is the LEGO of data pipelines.

![Monolithic_vs_modular_pipeline](https://github.com/amphoradata/samples/blob/master/modular_data_pipeline/Monolithic_vs_modular.png "Monolithic vs modular pipeline")

In contrast, traditional monolithic data pipelines are built as one long body of work. They are robust and efficient at their job. But everything is custom made and designed and hard to change or reuse.

## What are the benefits?

MDPs have lots of benefits including:
* More reusability
* More reliability
* Better security

These provide **higher uptime**, **less risk**, **lower cost**, and **faster time-to-market**.

### More reusability

MDP components can be reused across multiple data pipelines. In a similar manner to APIs, they can be dropped into any pipeline and do the same job they were initially designed to do.

For example, let's say we want to select an area of interest with a SHP/KML file from a GeoTIFF. We can drop in a `Get_AOI_from_GeoTIFF` MDP from our library of MDPs to do the job.

### More reliability

Each MDP component is designed for one thing and one thing only. That means it does that job very well with high reliability. 

In contrast, a monoloithic data pipeline is very sensitive to changes in source data and can break very easily. Of course their reliability can be improved but, like all monoloithic architecture, suffers from complexity and lack of agility as it gets bigger and bigger.

### Better collaboration

MDPs support better collaboration for teams. Components can be owned by different teams or even third-parties. With suitable platforms, like Amphora, data access and tracability can be done on a component by component so you know who has accessed which data.

Combined with an open-source collaboration platform, e.g. GitHub, MDPs enable teams to collaborate on a single data pipeline. This is very handy for research teams across multiple organisations, contractor/consultant teams as well as open source projects.

## How do they work with the Amphora Data platform?

Modular Data Pipelines naturally work very well on Amphora as we use data containerisation to store data. Each data pipeline can start and/or end in an Amphora.

PICTURE ON HOW THIS WORKS

## Sounds good, what do I need to start coding?

