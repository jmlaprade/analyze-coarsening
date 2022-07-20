# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:47:20 2022

@author: Jeremy Laprade

"""
##############################################################################
#                                USER INPUT                                  #

#specify data path and required information
#path that contains folders that contain raw data
directory = 'E:\\3D Active Coarsening\\Quality Data\\'
path = directory+'Parafilm Channels\\Varied KSA\\'

experiment = '22-04-07_10x_60sInt_14uMatp_orcaCam_20C_1\\'
pos = [
    '50nM',
    '100nM',
    '300nM',
    '500nM',
    ]
labels = [
    '50nM [KSA]',
    '100nM [KSA]',
    '300nM [KSA]',
    '500nM [KSA]',
    ]

#                               END USER INPUT                               #
##############################################################################

import numpy as np
import matplotlib.pyplot as plt

for i in range(len(pos)):
    resultPath = path+str(experiment)+'\\Results\\'+pos[i]+'\\'
    
    data = np.loadtxt(
        resultPath+'processedResults.log', 
        delimiter='|',
        skiprows=2,
        dtype='float',
        )
    
    plt.figure(0)
    plt.loglog(
        data[:,0],
        data[:,1],
        label=str(labels[i]),
        linewidth=3,
        )
    plt.loglog([2000, 8000], 0.25*np.array([2000,8000])**(1/3),'k')
    plt.xlabel('time, t (s)')
    plt.ylabel('avg. radius, $<R>$ ($\\mu$m)')
    axes = plt.gca()
    axes.tick_params(axis='x', labelsize=14)
    axes.tick_params(axis='y', labelsize=14)
    plt.legend()
    plt.legend(prop={'size':14})
    plt.figure(1)
    plt.plot(
        data[:,0],
        data[:,4],
        label=str(labels[i]),
        linewidth=3,
        )
    plt.xlabel('time, t (s)')
    plt.ylabel('fit paramater $\\mu$')
    axes = plt.gca()
    axes.tick_params(axis='x', labelsize=14)
    axes.tick_params(axis='y', labelsize=14)
    plt.legend()
    plt.legend(prop={'size':14})
    plt.figure(2)
    plt.plot(
        data[:,0],
        data[:,5],
        label=str(labels[i]),
        linewidth=3,
        )
    plt.xlabel('time, t (s)')
    plt.ylabel('fit paramater $\\sigma$')
    axes = plt.gca()
    axes.tick_params(axis='x', labelsize=14)
    axes.tick_params(axis='y', labelsize=14)
    #plt.legend()
    #plt.legend(prop={'size':14})