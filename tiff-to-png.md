In this example, we show you how to create a nice png raster image from a geotiff file. This code is predominatley written in python with some sections in R. 

## We will do this in three steps
1. Create table of geotiff (R)
2. Create raster in png (python)
3. Create label/legend (R)

## Detailed steps
### 1. Create table of geotiff (R)
We use R for this step as we found it more effective and robust than python for .tif and .tiff files.

First import the librarys you need

`library("raster")`

`library("rgdal")`

Now define the input and output file paths

`input_filepath <- Input_filepath_string`

`output_filepath <- Output_filepath_string`

Now load in the data set

`mytif <- raster(input_filepath)`

`spts <- rasterToPoints(mytif, spatial = TRUE)`

Create a projection from the latitude and logitude of the geotiff

`llprj <-  "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs +towgs84=0,0,0"`

`llpts <- spTransform(spts, CRS(llprj))`

Now transform the projection into a table

`x <- as.data.frame(llpts)`

Finally write the table to csv

`write.csv(x, output_filepath)`


### 2. Create raster in png (python)
First import the librarys you need

`import matplotlib.pyplot as plt`

`import numpy as np`

`import pandas as pd `

We first set some parameters for the location/address/date that we are looking at

`Dat_str = Date of image`

`Address = Address of image`

`separator = '_'`

`dat_sep = " "`

`lat_tl = Latitude of top left corner`

`lon_tl = Longtitude of top left corner`

`lat_br = Latitude of bottom right corner`

`lon_br = Logtitude of bottom right corner`

You then need to read in the csv from step 1. You may want to do this within a single file and call the array

`Original_csv = pd.read_csv(separator.join([Address,Dat_str,'High_Res_NDVI_array.csv']), sep=',')`

Create a numpy array

`Original_array = Original_csv.to_numpy()`

Make all the 0s transparent

`Img_array = np.ma.masked_equal(Img_array,0)`

Now create a plot of the image

`plt.figure(figsize = (24,12), dpi=80)`

`im = plt.imshow(Array_NDVI,cmap=cm)`

`plt.axis('off')`

Now export the image as a png

`plt.savefig(dat_sep.join([separator.join(['Lat',lat_tl,'Lon',lon_tl,'Lat',lat_br,'Lon',lon_br,'NDVI_High_Res_Colour',Dat_str]),'.png']),bbox_inches='tight',transparent = 'True')`

### 3. Create label/legend (R)
For most uses, you will need to create a legend for your image. We do this separately as you will likely update the rasters far more often, and you may want to fix a legend in a specific location
We will do this in python

First, import the librarys you will need

`import pylab as pl`

`import numpy as np`

`from matplotlib.colors import LinearSegmentedColormap`

Now create a dummy min_val to max_val array to create the colour bar with

`a = np.array([[min_val,max_val]])`

Then create the appropriate figure
`pl.figure(figsize=(9, 1.5))`

`img = pl.imshow(a, cmap = cmap)`

`pl.gca().set_visible(False)`

`cax = pl.axes([0, 0.2, 0.1, 1])`

`cb = pl.colorbar(cax = cax)`

Set the labels and ticks to white so it is easy to see on a satellite image
`cb.set_label(label = 'Label', size = 'large', weight = 'bold', color = 'white')`

`cb.ax.tick_params(labelsize = 'large', labelcolor = 'white')`

`cb.ax.yaxis.set_tick_params(color = 'white')`

Then export your colourbar as a png to use as you need

`pl.savefig("Your_label_colourbar.png",bbox_inches='tight',transparent = 'True')`

### Queries and comments
If you have any queries or comments on this sample code, please use GitHub or reach out to isaac@amphoradata.com 
