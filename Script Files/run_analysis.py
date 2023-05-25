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
from os import listdir, makedirs
from file_manager_functions import (
    filepath_setup, 
    create_outputs,
    read_paths,
    )

#change to 1 to allow for overwriting of previous data
overwriteData = 0

#the length of a pixel in microns for the camera
cameraPxSize = 6.5

# filepath to data storage (is hardcoded for your PC)
commonPath = 'E:\\Coarsening Data\\Droplets\\'

# create list of strings of each experiment in folder
fullExperimentList = read_paths(commonPath)

#begin loop over all experiments
for i in range(len(fullExperimentList)):
    #select experiment from experiment list
    currentExp = fullExperimentList[i]
    
    #determine whether analysis was already completed for this experiment
    analysisDone = exists(commonPath + currentExp + '\\completeResults.txt')
    
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
        sequence = read_paths(filepath)
        
        #remember to remove metadata
        nImages = len(sequence)
        
        #calculate the number of time points in the data set based on nZ
        nTimePoints = np.floor(nImages / int(nZ))
        #calcuate time array
        time = timeInterval*np.linspace(
            0,nTimePoints-1,nTimePoints) - quenchTime
        
        #begin loop over each time point in the experiment
        for t in range(nTimePoints):
            
        #will need to rename result file when done with analysis
        #os.rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None)
