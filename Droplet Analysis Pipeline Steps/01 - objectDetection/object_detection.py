# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 19:00:32 2022

@author: Jeremy Laprade
         Martin Fisher School of Physics
         Brandeis University
"""
##############################################################################
#                                USER INPUT                                  #

#specify data path and required information
#path that contains folders that contain raw data
directory = 'E:\\3D Active Coarsening\\Quality Data\\'
path = directory+'Parafilm Channels\\Varied KSA\\'
experiment = '22-04-07_10x_60sInt_14uMatp_orcaCam_20C_1\\'
#folder name that specifically contains image data
pos = '300nM'

#                               END USER INPUT                               #
##############################################################################

from skimage import io
from detection_functions import (
    binarize_gradient,
    measure_droplets,
    )
import numpy as np
from PIL import Image
from os import listdir, makedirs
from skimage.util import img_as_ubyte

#automatically creates full path
dataPath = path+experiment+pos+'_grad\\'

# make file paths to save binary datas 
binaryDir = path+experiment+pos+'_binary\\'
makedirs(
        binaryDir,
        exist_ok=True,
        )

# make file paths to save binary datas 
distDir = path+experiment+'Results\\'+pos+'\\Distributions\\'
makedirs(
        distDir,
        exist_ok=True,
        )

#get how many images exist to determine number of time points for 'for' loop
sequence = listdir(dataPath)
#determine number of frames in dataset
frames = len(sequence)

for t in range(frames):
    #import image t in the stack
    gradient = io.imread(
        dataPath+'gradient_'+str(t)+'.tif',
        )
    
    #binarize gradient image to individual regions
    binaryImage = binarize_gradient(
        gradient,
        blockSize=21,
        globalSensitivity=0.5,
        )
    binary = Image.fromarray(img_as_ubyte(binaryImage))
    binary.save(binaryDir+'binary_'+str(t)+'.tif')
    
    #get properties of image in pandas table format
    radius = measure_droplets(
        binaryImage,
        watershed=0,
        peakSearchRegion=3,
        )
    
    np.savetxt(
        distDir+'\\radiusDist_'+str(t)+'.txt',
        radius,
        fmt='%.3f')