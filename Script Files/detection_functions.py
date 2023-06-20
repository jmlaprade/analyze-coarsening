# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 20:56:08 2022

@author: Jeremy Laprade
         Martin Fisher School of Physics
         Brandeis University
"""
import numpy as np

def binarize_gradient(gradient,windowSize=9,detectionSensitivity=5):
    #from skimage import util
    #from custom_adaptives import bernsen
    import skimage.filters as filt
    from scipy.ndimage.morphology import (
        binary_fill_holes,
        binary_opening,
        binary_erosion,
        )
    from skimage.morphology import (
        skeletonize,
        remove_small_objects,
        )
    
    thresholdValues = filt.threshold_local(
        gradient,
        block_size=windowSize,
        method='gaussian',
        offset=-np.median(gradient)/(1E-10+detectionSensitivity)
        )

    gradientMask = (gradient) > (thresholdValues)
    edges = skeletonize(gradientMask)
   
    floodFill = binary_fill_holes(edges)
   
    finalMask = remove_small_objects(
        binary_erosion(floodFill),
        min_size=7,
        )

    return finalMask

def measure_droplets(mask):
    from skimage.measure import regionprops, label
    
    #label unique elements of mask
    labels = label(mask)
    
    #measure the properties of droplets
    stats = regionprops(
        labels, 
        intensity_image=None, 
        cache=True, 
        )
    if np.size(stats) == 0:
        droplets = np.array([])

    if np.size(stats) != 0:
        area = np.array([r.area for r in stats])
        radius = np.sqrt(area/np.pi)
        pos = np.array([r.centroid for r in stats])
        majorAxis = np.array([r.axis_major_length for r in stats])
        minorAxis = np.array([r.axis_minor_length for r in stats])
        AR = majorAxis/minorAxis
        
        #combine all arrays into single array
        dropletTuple = (pos,
                        radius.reshape(np.size(radius),1), 
                        AR.reshape(np.size(radius),1))
        droplets = np.hstack(dropletTuple)
    
    return droplets