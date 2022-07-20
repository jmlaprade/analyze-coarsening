# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 13:18:49 2022

@author: Jeremy
"""
from data_processor_functions import lognormal
import matplotlib.pyplot as plt

def plot_lognormal_hist(x,y,mu,sigma,savePath, index):
    fig = plt.figure()
    plt.plot(
        x,
        y,
        '.k',
        markersize=15,
        label='Measured distribution'
        )
    plt.plot(
        x,
        lognormal(
            x,
            mu,
            sigma,
            ),
        '-r',
        linewidth=3,
        label='Log-normal fit'
        )
    plt.xlabel('scaled radius, $\\bar{R}$')
    plt.ylabel('probability density, p($\\bar{R}$)d$\\bar{R}$')
    axes = plt. gca()
    axes.tick_params(axis='x', labelsize=14)
    axes.tick_params(axis='y', labelsize=14)
    plt.legend(prop={'size':14})
    fig.set_size_inches(7, 6)
    plt.savefig(fname=savePath+'distribution_fit_'+str(index)+'.png')
    plt.close()