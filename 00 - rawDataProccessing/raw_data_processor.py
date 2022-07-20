# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:28:25 2022

@author: Jeremy Laprade
         Martin Fisher School of Physics
         Brandeis University
"""
##############################################################################
#                                USER INPUT                                  #

#specify data path and required information
#path that contains folders that contain raw data
directory = 'E:\\3D Active Coarsening\\'
path = directory+'Parafilm Channels\\Varied KSA\\'
experiment = '{Enter experiment folder here.}\\'
#folder name that specifically contains image data
pos = '{Enter folder here.}'
#specify how many z-images are at each time point 
    #NOTE: number of z images times number of time points needs to equal the 
    # TOTAL number of images in the folder
nZ = 12

#                               END USER INPUT                               #
##############################################################################

from processing_functions import (
    import_zstack, 
    gradient_zstack,
    )
import numpy as np
from os import listdir, makedirs
from PIL import Image
from skimage.util import img_as_ubyte

#automatically creates full path
dataPath = path+experiment+pos+'\\'
# make file paths to save processed datas 
intensityDir = path+experiment+pos+'_int\\'
makedirs(
        intensityDir,
        exist_ok=True,
        )
gradientDir = path+experiment+pos+'_grad\\'
makedirs(
        gradientDir,
        exist_ok=True,
        )
#get how many images exist to determine number of time points for 'for' loop
sequence = listdir(dataPath)
#subtract 1 becuase metadata.txt exists and is always last in the order
nImages = len(sequence)-1
#number of time points is total images / number of images per time point
frames = int(nImages/nZ)
for t in range(frames):
    #import entire stack at time point t
    stack = import_zstack(dataPath, t, nZ)
    #get the max intensity projection
    maxIntensity = np.amax(stack, 2)
    intNorm = np.max(maxIntensity)
    intensity = Image.fromarray(
        img_as_ubyte(
            maxIntensity/intNorm
            )
        )
    intensity.save(intensityDir+'intensity_'+str(t)+'.tif')
    #get the max gradient projection, calculating gradient FIRST
    gradMag = gradient_zstack(stack, nZ)
    maxGradMag = np.amax(gradMag, 2)
    gradNorm = np.max(maxGradMag)
    gradient = Image.fromarray(
        img_as_ubyte(
            maxGradMag/gradNorm
            )
        )
    gradient.save(gradientDir+'gradient_'+str(t)+'.tif')