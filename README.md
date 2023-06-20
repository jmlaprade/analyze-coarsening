# Coarsening analysis README

Script for analyzing coarsening of bright droplets on a dark background.  Assumes all droplets are images via z-scan.

To run analysis on many different experiments at once, the data must be organized in a specific way, with particular information in the filename.  
Each set of raw data must be located in its own folder with all properties relevant to the experiment listed in the folder name.  
Each experiment to be analyzed should be located within the same folder.

The template for naming experiment folders is: yy-mm-dd_#-activity_###-h_###-atp_###-ns_##-obj_###-int_###-t0-##-nZ_#.
The parameters are separated by an underscore. 
These parameters are:
1. Date, in year-month-day format with dashes between each element.
2. Whether the sample is active or not, should be 1 (0) for active fluid (passive fluid) samples.
3. The height of the sample chamber in microns, should be three digits (for 50um, write "050-h")
4. The ATP concentration, in micromolar (three digits).
5. The nanostar concentration, in micromolar (three digits).
6. The objective magnification (two digits, if 4x, write "04-obj")
7. The time interval between images, in seconds.  (three digits).
8. The number of images in each time point (e.g. how many images in the z-scan, two digits)
9. Trailing number to differentiate experiments with exact same parameters carried out on the exact same day. (One digit).

Inside each experiment folder, there should be a folder named "Raw Data" that contains un-altered image files of only the droplets.  
If there is another channel imaged (for example microtubules), take them out and store in a seperate folder in the same folder as the experiment folder.
