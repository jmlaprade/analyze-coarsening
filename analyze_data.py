# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:33:29 2022

@author: Jeremy Laprade
     Duclos Lab
     Martin Fisher School of Physics
     Brandeis University
"""
def coarsening_loop(directory, experiment, labels, parameters):

# ----------------------------------------------------------------------------
# import packages
# ----------------------------------------------------------------------------
    
    import numpy as np
    from os import listdir
    from skimage import io
    from os import makedirs
    import imageio
    import matplotlib.pyplot as plt
    
    from binarization_functions import edge_binarization
    from droplets_analysis_functions import (
        get_droplet_stats, 
        plot_histogram,
        )

# ----------------------------------------------------------------------------
# derived parameters
# ----------------------------------------------------------------------------

    px = parameters[0]
    obj = parameters[1]
    dt = parameters[2]
    pxConv = px/obj
    pxConv2 = pxConv*pxConv 
    dt = parameters[2]
    reducFactor = 20

# ----------------------------------------------------------------------------
# directories
# ----------------------------------------------------------------------------

    dataFilePath = directory+experiment+'\\DNA\\'
    images = listdir(dataFilePath)
    
    #make directory for saving binary images
    binary_dir = directory+experiment+'\\Binaries\\'
    makedirs(
            binary_dir,
            exist_ok=True,
            )
    
    #make directory for saving results
    results_dir = directory+experiment+'\\Coarsening\\'
    makedirs(
            results_dir,
            exist_ok=True,
            )
    
    #make directory for saving distributions
    dist_dir = results_dir+'\\DistData\\'
    makedirs(
            dist_dir,
            exist_ok=True,
            )
    
    #make directory for saving results
    plots_dir = results_dir+'\\DistPlots\\'
    makedirs(
            plots_dir,
            exist_ok=True,
            )
    
    #make directory for saving results
    save_dir = directory+'\\Results\\'+experiment+'\\'
    makedirs(
            save_dir,
            exist_ok=True,
            )

# ----------------------------------------------------------------------------
# main analysis functions
# ----------------------------------------------------------------------------

    #determine number of points to analyze
    nPoints = int(np.floor(len(images)/reducFactor))
    
    #initialize data arrays
    time = np.zeros(nPoints)
    avg_R = np.zeros(nPoints)
    N = np.zeros(nPoints)
    V_tot = np.zeros(nPoints)
    mu = np.zeros(nPoints)
    sigma = np.zeros(nPoints)
    
    for i in range(nPoints):
        #wourk out correct time variable and store it
        t = i*reducFactor
        time[i] = t*dt
        
        # read image to analyze
        data = io.imread(
            dataFilePath+images[t],
            )
        
        #binarize image using custom edge based algorithm and save the data
        binary = edge_binarization(
            data, 
            blurMult=5, 
            thStrength=0.5,
            )
        imageio.imwrite(
            binary_dir+'binary_'+str(t)+'.tif', 
            1*binary,
            )
        
        #get distribution of dropelt radii in microns
        radiusDist = get_droplet_stats(binary)*pxConv2
        
        #plot histogram and fit histogram after 30 min of imaging
        if t*dt > 500:
            popt = plot_histogram(radiusDist)
            plt.savefig(plots_dir+'distribution_'+str(t*dt)+'sec.png')
            plt.close()
            
            sigma[i] = popt[0]
            mu[i] = popt[1]
    
        #calculate statistics of droplet distributions
        V = (4*np.pi/3)*radiusDist**3
        V_tot[i] = np.sum(V)
        N[i] = len(radiusDist)
        avg_R[i] = np.mean(radiusDist)
        
        #write distribution to a text file
        np.savetxt(
            dist_dir+'radii_'+str(t)+'.txt', 
            radiusDist,
            fmt = '%1.3f'
            )
        
        #append results in text file
        dataLog = open(
            save_dir+'results.txt', 'a'
            )
        dataLog.write(
            str(t*dt)+' , '+str(avg_R[i])+' , '+str(N[i])+' , ' 
            +str(V_tot[i]) + ' , '+str(mu[i])+' , '+str(sigma[i])+'\n')
        dataLog.close()
