# introduction

This group of files should allow you to analyze large batches of data automatically from raw data, organized in a specific way.

# data organization
The current analysis pipeline requires the data to be organized in a particular way. All data that is supposed to be analyzed should all be on the same disk. For example, you may store all your data folders in a location such as "E:\MyDataDirectory\". This will wind up being your "dataDirectory" string in the main pipeline file. 

Your experiment names are simply the folders which contain a folder that contains your images. The folder that contains the images should be called "DNA" (This can be changed in the files later if it becomes more applicable to other projects). For example, you might aquire a set of data that ImageJ saves in a single folder ("Default", usually).  You should seperate the droplet images from microtubule images before running the pipeline on the data.  The full path to the data should then look something like this: "E:\MyDataDirectory\ExperimentName\DNA\dataImages".  

When analyzing more than one experiment at once, you should have your data organized like this:
"E:\MyDataDirectory\ExperimentName1\DNA\dataImages" 
"E:\MyDataDirectory\ExperimentName2\DNA\dataImages"
"E:\MyDataDirectory\ExperimentName3\DNA\dataImages"... 

Experiment labels are the names associated to the experiment that will show up in plot legends.

Experiment parameters are the pixel size of the camera used, the objective magnification, and the imaging period in seconds.


Functionality to add in the future...
- Currently, a factor is hardcoded into the pipeline that reduces the number of images analyzed for each experiment (currently it analyzes every 20 images, but STILL KEEP THE ORIGINAL IMAGING PERIOD, dt is automatically updated based on this number).  We may want to make this a user input.
- I want to devise some parameter that automatically deduces what interval to perform fitting to average radius and number over time. Currently, my idea would that we should wait until droplets have all fallen down to the interface.  Two options to examine that would be to look at when the total droplet volume becomes constant over time, but this is suseptible to large noise if big droplets are leaving and entering the feild of view. Alternatively, we can look at how much of the image is blurry.  When very few objects are blurry, we might then say that the droplets have all settled at the bottom and we can examine the coarsening rate from there.
- Need some function to compile PIV results from matlabs PIVlab program to automatically compare fitted beta values to flow parameters
