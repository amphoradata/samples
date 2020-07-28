# Modular data pipelines improve reusability and reliability for ETL and analytics

Pipelines route data from a source to a destination. All analytics and extract-transform-load (ETL) involve them. Pipelines come in all shapes and sizes but modular pipelines can be best if you are working collaboratively, without too much legacy tech, and have a big backlog of similar but different data and analytics tasks.

This readme is a companion to a video and all code is in this GitHub repo.

## What exactly is a modular data pipeline?

A modular data pipeline (MDP) is a process to move or transform data that is broken down into the smallest steps possible. Each of these steps is a very small data pipeline component that, when added together, form a larger data pipeline. Essentially it is the LEGO of data pipelines.

<img src="https://github.com/amphoradata/samples/blob/master/modular_data_pipeline/Monolithic_vs_modular.png" width="800" title = "Monolithic vs modular pipeline">

In contrast, traditional monolithic data pipelines are built as one long structure. They are robust and efficient at their job. But everything is custom made and designed and can be hard to change or reuse.

## What are the benefits?

MDPs have lots of benefits including:
* More reusability
* More reliability
* Better collaboration

These help you get **higher uptime**, **less risk**, **lower cost**, and **faster time-to-market**.

### More reusability

Modular Data Pipeline components can be reused across multiple data pipelines. In a similar manner to APIs, they can be dropped into any pipeline and do the same job they were initially designed to do.

For example, let's say we want to select an area of interest with a SHP/KML file from a GeoTIFF. We can drop in a `Get_AOI_from_GeoTIFF` MDP from our library of MDPs to do the job.

MDPs have high mutability. If you upgrade a model or want to pull in different data, you can simply replace or upgrade a component. 

### More reliability

Each MDP component is designed for one thing and one thing only. That means it does that job very well with high reliability. MDPs also easily align with the `Single Responsibility Principle`. A library of MDP components should only change if there is a data format change. 

In contrast, a monoloithic data pipeline is very sensitive to changes in source data and can break very easily. Of course their reliability can be improved but, like  monoloithic stacks, can suffer from complexity and lack of agility as it gets bigger and bigger.

### Better collaboration

Modular Data Pipelines support better collaboration for teams. Components can be owned by different teams or even third-parties. With suitable platforms, like Amphora, data access and tracability can be done on a component by component basis so you know who has accessed which data.

Combined with an open-source collaboration platform, e.g. GitHub, MDPs enable teams to collaborate on a single data pipeline. This is very handy for research teams across multiple organisations, contractor/consultant teams as well as open source projects.


## How do they work with the Amphora Data platform?

Modular Data Pipelines naturally work very well with Amphora as we use data containerisation to store data. Each data pipeline can start and/or end in an Amphora. MDP components can refer to any Amphora with the unique `amphora_id`. We find it best to call the `amphora_id` in the `run.py` and pass an Amphora object to each component.

We typically use a three stage MDP for our data pipelines. The first stage is to transfer of raw data from a source Amphora to a workspace Amphora. Second stage is to do any enrichment, cleaning, manipulation, analytics, that needs to happen. The last stage is to present the data in the format our customers want. This is analogous to source system, data lake, and interaction layer in enterprise software.

<img src="https://github.com/amphoradata/samples/blob/master/modular_data_pipeline/Amphora_MDB_example.JPG" width="800" title = "Amphora MDP example">

## Sounds good, what do I need to start coding?

Its easy to get started with MDPs. Simply
1. Choose your interface standard
2. Design your MDP
3. Make the components
4. Plug them all together

### 1. Choose your interface standard

You need to choose your standard data type, filename format, and data storage locations. These don't need to be set in stone but most components should pipe these.

In our data science team, we typically use `.csv`s for our files, `propertyId_YYMMDD_DATACONTENT` for filenames, and naturally Amphoras to store data. That said, we process all types of files and filenames but we try to convert them to our standard for as many components as possible.

There is clearly a dependency on the schema set in Step 1. Its worthwhile taking time and setting this for your best needs.

> LEGO step: Set the standard block hight and circle size
<img src="https://github.com/amphoradata/samples/blob/master/modular_data_pipeline/lego_pic_1.png" width="300" title = "Set the standard block hight and circle size">

### 2. Design your MDP

You now need to design your MDP. When designing components, try to use small and logical functions that are parameterised for varied situations. Designing for reusability can save time too. We aim to reuse over 70% of our components in other data pipelines. This saves us both developer time and maintenance effort.

You should use a reference architecture or capability map that best suits you. Our data science team typically uses a three stage approach: raw-to-working, working, working-to-finished-product. We use three different Amphoras for each of these. We use different Amphoras as we can set different restrictions for each Amphora, reuse raw data in multiple analytics products, and use the same working MDP components for different customers and datasets. 

For example, we use components such as 
* `tiff_to_ndvi`: This takes a tiff image and creates and ndvi csv
* `identify_vines`: This identifies all the pixels which contain grape vines in a satellite image
* `publish_overall_image`: This takes a csv and creates a standard png image

> LEGO step: Design your LEGO model and write instructions
<img src="https://github.com/amphoradata/samples/blob/master/modular_data_pipeline/lego_pic_2.JPG" width="300" title = "Design your LEGO model and write instructions">

### 3. Make the components

Now you need to start writing the code in each component. This is obviously dependent on your own needs but try to use 5 lines or less of actual data manipulation, cleaning, engineering, or analytics to keep your component as small as possible.

One of our components computes the change in NDVI between two images. The code is simply
```py
  ndvi_array = np.array(ndvi_masked_csv.to_numpy())
  ndvi_prev_array = np.array(ndvi_masked_prev_csv.to_numpy())

  change_in_ndvi_csv = ndvi_array - ndvi_prev_array
```

> LEGO step: Make the small parts of a LEGO model
<img src="https://github.com/amphoradata/samples/blob/master/modular_data_pipeline/lego_pic_3.jpg" width="300" title = "Make the small parts of a LEGO model">

### 4. Plug them all together

Now you need to add all your components together into a single pipeline run file. This is pretty standard and can be set to do `batch`, `on-demand`, `scheduled` or whatever you need to do.

> LEGO step: Put all bits together to have a complete model
<img src="https://github.com/amphoradata/samples/blob/master/modular_data_pipeline/lego_pic_4.jpg" width="300" title = "Put all bits together to have a complete model">

## Questions?

Send us an [email](mailto:contact@amphoradata.com)
