# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:12:44 2022

@author: Jeremy
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 23:17:57 2022

@author: Jeremy Laprade
"""

def import_zstack(path, index, nz):
    from skimage import io
    from os import listdir
    import numpy as np
    from skimage import util
    
    imageStack = np.zeros((2048, 2048, nz))
    sequence = listdir(path)
    
    for z in range(nz):
        temp_image = io.imread(
            path+sequence[index*nz+z],
            )
        imageStack[:,:,z] = util.img_as_ubyte(temp_image)
    
    return imageStack

def gradient_zstack(stack, nFrames):
    import numpy as np
    from skimage.filters import sobel
    from scipy.ndimage import gaussian_filter
     
    gradientMagnitude = np.zeros((2048, 2048, nFrames))
    for i in range(nFrames):
        filteredImage = gaussian_filter(stack[:,:,i],sigma=np.sqrt(2))
        gradientMagnitude[:,:,i] = sobel(filteredImage)
        
    return gradientMagnitude

def binarize_gradient(intensityData, gradientData, n):
    #from skimage import util
    #from custom_adaptives import bernsen
    import skimage.filters as filt
    from skimage import util
    from scipy.ndimage.morphology import (
        binary_fill_holes,
        binary_closing,
        binary_opening,
        )
    import numpy as np
    from skimage.morphology import skeletonize

    #perform adaptive threshold with large window size
    adaptiveThres = filt.threshold_local(
        intensityData,
        block_size=15,
        method='gaussian',
        )

    adaptiveMask = intensityData>adaptiveThres
    
    gradThresh = np.mean(gradientData)+n*np.std(gradientData)
    adaptGradThresh = filt.threshold_local(
        gradientData,
        block_size=9,
        method='median'
        )
    filterBinary = gradientData > gradThresh
    binary = gradientData > adaptGradThresh
    skeleton = skeletonize(binary_opening(filterBinary*binary))
    mask = binary_opening(binary_fill_holes(skeleton))
        
    return mask, binary*filterBinary