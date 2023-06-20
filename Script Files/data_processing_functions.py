# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:12:44 2022

@author: Jeremy
"""
from skimage import io
from os import listdir
import numpy as np
from skimage.filters import sobel
from scipy.ndimage import gaussian_filter

def import_zstack(path, index, nz):
    
    imageStack = np.zeros((2048, 2048, nz))
    sequence = listdir(path)
    
    for z in range(nz):
        temp_image = io.imread(
            path+'\\'+sequence[index*nz+z],
            )
        imageStack[:,:,z] = temp_image
    return imageStack

def gradient_zstack(stack, nFrames, sigma):
    gradientMagnitude = np.zeros((2048, 2048, nFrames))
    for i in range(nFrames):
        filteredImage = gaussian_filter(stack[:,:,i],sigma=sigma)
        gradientMagnitude[:,:,i] = sobel(filteredImage)
    return gradientMagnitude

def zproject(block, nz):
    flat = np.amax(block, 2)
    return flat

def normalize_image(image):
    maxval = np.max(image)
    minval = np.min(image)
    normImage = (image-minval)/(maxval-minval)
    return normImage