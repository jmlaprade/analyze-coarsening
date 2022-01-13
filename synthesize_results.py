# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 14:36:40 2022

@author: Jeremy
"""
def consolidate_data(directory, experiment):
    from os import makedirs
    import numpy as np
    
    #make directory for consolidating results
    result_dir = directory+'\\Results\\'
    makedirs(
            result_dir,
            exist_ok=True,
            )
    data = np.loadtxt(
        directory+experiment+'\\Coarsening\\results.txt',
        delimiter=',',
        )
    saveString = result_dir+experiment
    np.savetxt(
        saveString+'\\result.txt', 
        data, 
        delimiter=',',
        )

def plot_results(directory, experiments, labels):
    import matplotlib.pyplot as plt
    import numpy as np
    from os import makedirs
    
    nIterations = len(experiments)
    plt.figure()
    #plot average radius over time on a log log scale
    for i in range(nIterations):
        data = np.loadtxt(
            directory+'\\Results\\'+experiments[i]+'\\results.txt',
            delimiter=',',
            )
        plt.loglog(data[:,0], data[:,1],label=labels[i])
    
    plt.xlabel('Time, $t$ (s)')
    plt.ylabel('Mean radius, $< R(t) >$ ($\mu$m)')
    plt.legend()
 
    plt.figure()
    #plot total volume over time 
    for i in range(nIterations):
        data = np.loadtxt(
            directory+'\\Results\\'+experiments[i]+'\\results.txt',
            delimiter=',',
            )
        plt.plot(data[:,0], data[:,3],label=labels[i])
    
    plt.xlabel('Time, $t$ (s)')
    plt.ylabel('Total volume, $V$ ($\mu$m$^3$)')
    plt.legend()
    
    plt.figure()
    #plot total volume over time 
    for i in range(nIterations):
        data = np.loadtxt(
            directory+'\\Results\\'+experiments[i]+'\\results.txt',
            delimiter=',',
            )
        plt.loglog(data[:,0], data[:,2],label=labels[i])
    
    plt.xlabel('Time, $t$ (s)')
    plt.ylabel('Number of droplets, N')
    plt.legend()
    
    plt.figure()
    #plot total volume over time 
    for i in range(nIterations):
        data = np.loadtxt(
            directory+'\\Results\\'+experiments[i]+'\\results.txt',
            delimiter=',',
            )
        plt.plot(data[:,0], data[:,5],label=labels[i])
    
    plt.xlabel('Time, $t$ (s)')
    plt.ylabel('Distribution width?, $\sigma$')
    plt.legend()