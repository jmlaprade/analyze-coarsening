# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 20:56:08 2022

@author: Jeremy Laprade
         Martin Fisher School of Physics
         Brandeis University
"""

def binarize_gradient(gradient, blockSize=9, globalSensitivity=0.5):
    from skimage.filters import (
        threshold_local, 
        threshold_otsu,
        )
    from skimage.morphology import (
        skeletonize,  
        )
    from scipy.ndimage import (
        binary_opening,
        )
    from scipy.ndimage.morphology import binary_fill_holes
    
    #get global threshold value from Otsu method, modulate by sensitivity 
    #parameter
    thresholdGlobal = globalSensitivity*threshold_otsu(gradient)
    binaryGlob = gradient > thresholdGlobal
    
    #perform local thresholding on gradient
    thresholdLocal = threshold_local(
        gradient, 
        block_size=blockSize,
        method='gaussian'
        )
    binaryLoc = gradient > thresholdLocal
    
    #combine global and local thresholds by multiplication, then skeletonize
    outlineRaw = skeletonize(binaryGlob*binaryLoc)
    
    #fill holes in image, then remove excess lnes
    finalBinary = binary_opening(
        binary_fill_holes(
            outlineRaw,
            ),
            iterations=2, 
        )
    
    return finalBinary

def measure_droplets(image, watershed=1, peakSearchRegion=3):
    import numpy as np
    from scipy import ndimage as ndi
    from skimage.segmentation import watershed
    from skimage.feature import peak_local_max
    from skimage.measure import regionprops
    
    # Now we want to separate the two objects in image
    # Generate the markers as local maxima of the distance to the background
    distance = ndi.distance_transform_edt(image)
    coords = peak_local_max(
        distance, 
        footprint=np.ones((peakSearchRegion, peakSearchRegion)), 
        labels=image
        )
    
    mask = np.zeros(
        distance.shape, 
        dtype=bool
        )
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    
    labels = watershed(
        -distance, 
        markers, 
        mask=image
        )
    
    stats = regionprops(
        labels, 
        intensity_image=None, 
        cache=True, 
        )
    
    area = np.array([r.area for r in stats])
    radius = np.sqrt(area/np.pi)
    
    return radius