# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:10:17 2023

@author: Jeremy Laprade | Brandeis University

    Script to analyze and store results for dropelt coarsening experiments.
    Will automatically analyze all folders which have not been analyzed yet
        (unless overidden)
    Experiment folders must have the following format:
    yy-mm-dd_#-activity_###-h_###-atp_###-ns_##-obj_###-int_###-t0-##nZ_#
         (see readme for detailed file formatting requirements, units, etc)
    
"""
import numpy as np
from os.path import exists
from os import listdir, makedirs, rename
from skimage import io
from PIL import Image
from skimage.util import img_as_ubyte

import time

# from file_manager_functions import (
#     filepath_setup, 
#     create_outputs,
#     read_paths,
#     )
from data_processing_functions import (
    import_zstack, 
    gradient_zstack,
    zproject,
    normalize_image,
    )
from detection_functions import (
    binarize_gradient,
    measure_droplets,
    )

#change to 1 to allow for overwriting of previous data
overwriteData = 0

#the length of a pixel in microns for the camera
cameraPxSize = 6.5

# filepath to data storage (is hardcoded for your PC)
commonPath = 'E:\\Coarsening Data\\Droplets\\'

# create list of strings of each experiment in folder
fullExperimentList = listdir(commonPath)

#begin loop over all experiments
for i in range(len(fullExperimentList)):
    #output what experiment is being worked on now
    print('Working on experiment '+str(i)+' of '+str(len(fullExperimentList)))
    #select experiment from experiment list
    currentExp = fullExperimentList[i]
    
    #determine whether analysis was already completed for this experiment
    analysisDone = exists(commonPath + currentExp + '\\completeResults.log')
    
    if analysisDone == False:
        #assemble path to folder with raw data files for this experiment
        dataFolder = commonPath + currentExp + '\\Raw Data\\'

        #assemble path to folder with binary data files for this experiment
        binaryFolder = commonPath + currentExp + '\\Binary Data\\'
        makedirs(
            binaryFolder,
            exist_ok=True,
            )
        #assemble path to folder with intensity data files for this experiment
        intensityFolder = commonPath + currentExp + '\\Intensity Data\\'
        makedirs(
            intensityFolder,
            exist_ok=True,
            )
        #assemble path to folder with distribution files for this experiment
        distributionFolder = commonPath + currentExp + '\\Distribution Data\\'
        makedirs(
            distributionFolder,
            exist_ok=True,
            )
        
        #split folder name by underscores into each parameter
        currentExpParams = currentExp.split("_")
        
        #collect all parameters in string format
        activity = currentExpParams[1].split("-")[0]
        channelHeight = currentExpParams[2].split("-")[0]
        atpConc = currentExpParams[3].split("-")[0]
        nsConc = currentExpParams[4].split("-")[0]
        objectiveMagnification = currentExpParams[5].split("-")[0]
        timeInterval = currentExpParams[6].split("-")[0]
        quenchTime = currentExpParams[7].split("-")[0]
        nZ = currentExpParams[8].split("-")[0]
        
        # calculate the pixel to micron conversion ratio
        pxConv = cameraPxSize / int(objectiveMagnification)
        #read the names of images into a sequence of files
        sequence = listdir(dataFolder)
        
        #remember to remove metadata
        nImages = len(sequence)
        
        #calculate the number of time points in the data set based on nZ
        nTimePoints = int(np.floor(nImages / int(nZ)))
        #calcuate time array
        timeArray = int(timeInterval)*np.linspace(
            0,nTimePoints-1,nTimePoints) - int(quenchTime)
        
        #create and open log file to output main results
        fLog = open(commonPath + currentExp + '\\incompleteResults.log', 'w')
        fLog.write("| Time | Avg R | Num Dens | Sigma | \n")
        fLog.write("|------|-------|----------|-------|\n")
        #begin loop over each time point in the experiment
        for t in range(nTimePoints):
            
            #output what frame is being worked on now
            #print('Working on frame '+str(t)+' of '+str(nTimePoints))

            #import z-stack of images (with 'nZ' images) at time point 't'
            stack = import_zstack(dataFolder, t, int(nZ))
                
            #calculate the max intensity projection
            flatIntensity = zproject(stack,int(nZ)) 
            
            #calculate the normalized image based on 16-bit range of values
            normIntensity = normalize_image(flatIntensity)
            
            #make intensity image an 8-bit file
            intensity = Image.fromarray(
                img_as_ubyte(normIntensity),
                )
            
            #save the intensity image to file
            intensity.save(intensityFolder+'intensity_'+str(t)+'.tif')
            
            #calculate the gradient of intensity on each image in the stack
            gradientStack = gradient_zstack(stack, int(nZ), sigma=2)
            
            #calculate z-projection of gradient stack
            flatGradient = zproject(gradientStack,int(nZ))
            
            #normalize gradient based on 16-bit range of values
            normGradient = normalize_image(flatGradient)
            
            if timeArray[t] > 0:
                #make binary image from gradient data
                binaryImage = binarize_gradient(
                    normGradient,
                    windowSize=9,
                    detectionSensitivity = 4, #larger values are more sensitive
                    )
                
                #make binary image an 8-bit file
                binary = Image.fromarray(img_as_ubyte(binaryImage))
                
                #save the binary to file
                binary.save(binaryFolder+'binary_'+str(t)+'.tif')
                
                #get list of object radii (based on total area calculation)
                droplets = measure_droplets(
                    binaryImage,
                    )
                
                #write distribution information to a text file
                np.savetxt(
                    distributionFolder+'detectionRawData_'+str(t)+'.txt',
                    droplets,
                    fmt='%0.2f',
                    )
                
                #calculate other important observables of the experiment
                step = timeArray[t]
                avgR = pxConv*np.mean(droplets[:,2])
                boxVolume = int(channelHeight)*(pxConv **2)*np.size(binaryImage,0)*np.size(binaryImage,1)
                numDens = np.size(droplets[:,2])/boxVolume
                sigma = np.std(np.log(pxConv*droplets[:,2]/avgR))
                
                fLog.write(f"| {step:>4} | {avgR:>0.3f} | {numDens:>1.2e} | {sigma:>0.3f} |\n")        
        
        #close file of data output
        fLog.close()
        
        #ensure file is closed before renaming by making a 60 second delay
        time.sleep(60)
        
        #rename file once analysis is done
        rename(
            commonPath + currentExp + '\\incompleteResults.log', 
            commonPath + currentExp + '\\completeResults.log',
            )
 