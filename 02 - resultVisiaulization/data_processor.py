# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 09:38:21 2022

@author: Jeremy Laprade
"""
##############################################################################
#                                USER INPUT                                  #

px = 0.65
dt = 1*60
t0 = 4*60
boxLengthPx = 2048
boxHeight = 100
binWidth = 0.1

#specify data path and required information
#path that contains folders that contain raw data
directory = 'E:\\3D Active Coarsening\\Quality Data\\'
path = directory+'Parafilm Channels\\Varied KSA\\'
experiment = '22-04-07_10x_60sInt_14uMatp_orcaCam_20C_1\\'
#folder name that specifically contains image data
pos = '300nM'

#                               END USER INPUT                               #
##############################################################################

import numpy as np
from os import listdir, makedirs
from data_processor_functions import(
    lognormal,
    lognormal_histfit,
    )
from data_plotting_functions import plot_lognormal_hist
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

px2 = px**2
px3 = px**3

#calculate box volume in microns
boxAreaPx = boxLengthPx**2
boxArea = boxAreaPx*px2
boxVolume = boxHeight*boxArea*px

#automatically creates full path for droplet distributions
distPath = path+experiment+'Results\\'+pos+'\\Distributions\\'
#make directory for distribution plots
distPlotPath = path+experiment+'Results\\'+pos+'\\Distribution Plots\\'
makedirs(
        distPlotPath,
        exist_ok=True,
        )
# make file paths to save processed results 
resultsDir = path+experiment+'Results\\'+pos

nFiles = len(listdir(distPath))

#initialize data arrays
distIndicies = [20,40,80,160,300,520]

print(" Time (s) | <R> (um) | # Drops | Vol Frac | Fit Mean | Fit Sdev " )
print("----------|----------|---------|----------|----------|---------")
#open file at start for writing...
fLog = open(resultsDir+'\\processedResults.log', 'w')
fLog.write("Time (s) | <R> (um) | # Drops | Vol Frac | Fit Mean | Fit Sdev \n")
fLog.write("---------|----------|---------|----------|----------|---------\n")

#fig = plt.figure()
for t in range(nFiles):
    time = dt*t - t0
    if time > 0:
        radius = px*np.loadtxt(distPath+'radiusDist_'+str(t)+'.txt')
        #perform calculations with the radius distribution
        
        N = np.size(radius)
        if N > 10:
            avgR = np.mean(radius)
            volume = (4*np.pi/3)*(radius**3)
            totalVolume = np.sum(volume)
            phi =   totalVolume/boxVolume
            
            scaledRadius = radius/np.mean(radius)
            maxVal = np.min([np.max(scaledRadius), 3])
            binCounts = int(np.floor((maxVal/binWidth)))
            #fit the radius distribution
            binCenters, pdf, mu, sigma = lognormal_histfit(
                radius/np.mean(radius), 
                binNumber = binCounts,
                )
            fitMean = np.exp(mu+(sigma**2)/2)
            fitStd = (np.exp(sigma**2)-1)*np.exp(2*mu+sigma**2)
            
            print(f"{time:>0.2e} | {avgR:>0.2e} | {N:>0.2e} | {phi:>0.2e} | {mu:>0.2e} | {sigma:>0.2e}")
            fLog.write(f"{time:>0.2e} | {avgR:>0.2e} | {N:>0.2e} | {phi:>0.2e} | {mu:>0.2e} | {sigma:>0.2e}\n")
            #plot and save droplet distribution and resulting fit
            plot_lognormal_hist(
                binCenters, 
                pdf, 
                mu, 
                sigma, 
                distPlotPath, 
                t,
                )
    
            if t in distIndicies:
                plt.plot(
                    binCenters, 
                    pdf,
                    '-',
                    label='t = '+str((t*dt-t0)/60)+'min',
                    #markersize=15,
                    linewidth=3,
                    )
                plt.xlabel('scaled radius, $\\bar{R}$')
                plt.ylabel('probability density, p($\\bar{R}$)d$\\bar{R}$')
                axes = plt.gca()
                axes.tick_params(axis='x', labelsize=14)
                axes.tick_params(axis='y', labelsize=14)
                plt.legend()
                plt.legend(prop={'size':14})
                #fig.set_size_inches(7, 6)



fLog.close()
