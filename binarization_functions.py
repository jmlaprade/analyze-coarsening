# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 13:43:47 2022

@author: Jeremy Laprade
         Duclos Lab
         Martin Fisher School of Physics
         Brandeis University
"""

def edge_binarization(image, blurMult=2,thStrength=1):
    
    import numpy as np
    from skimage import util
    from skimage.restoration import denoise_bilateral
    from skimage.filters import (
        threshold_local,
        threshold_otsu,
        roberts,sobel,
        scharr, 
        gaussian,
        )
    from skimage.morphology import skeletonize
    from scipy.ndimage.morphology import (
        binary_fill_holes,
        binary_opening, 
        )

    #ensure that image is in 8-bit format before beginning segmentation
    data = util.img_as_ubyte(image)
        
    intTH = threshold_local(
        data,
        block_size=15,
        method='mean'
        )
    intFilter = data > intTH
    
    #globalTH = threshold_otsu(data)
    
    #intFilter = (globalTH+localTH) > 1
    
    #run bilateral filtering on raw data
    blurSigma = blurMult*np.std(data)
    smoothData = denoise_bilateral(
        data, 
        sigma_color=blurSigma
        )
    
    # perform gradient filtering on smooth data and combine methods
    scharrFilter = scharr(smoothData)

    #use otsu threshold to binarize gradient map
    binaryGradient = scharrFilter > thStrength*threshold_otsu(scharrFilter)
    
    #skeletonize initial binary to get pixel wide edges
    skeletonBinary = skeletonize(binary_opening(binaryGradient))
    
    #fill holes to make initial binary map
    filledBinary = binary_fill_holes(skeletonBinary)
    
    #clean excess holes not filled
    cleanBinary = intFilter*binary_opening(filledBinary)
    binary = binary_fill_holes(cleanBinary)
    
    return binary