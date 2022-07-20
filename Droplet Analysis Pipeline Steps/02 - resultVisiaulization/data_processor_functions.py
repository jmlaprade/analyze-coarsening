# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 20:07:04 2022

@author: Jeremy Laprade
"""
from scipy.optimize import curve_fit
import numpy as np

def lognormal(x,mu,sigma):
    
    constant = 1/(x*sigma*np.sqrt(2*np.pi))
    numerator = (np.log(x)-mu)**2
    denominator = 2*sigma**2
    
    pdf = constant*np.exp(-numerator/denominator)
    
    return pdf

def normal(x,mu,sigma):
    
    constant = 1/(x*sigma*np.sqrt(2*np.pi))
    numerator = (np.log(x)-mu)**2
    denominator = 2*sigma**2
    
    pdf = constant*np.exp(-numerator/denominator)
    
    return pdf

def lognormal_histfit(distribution, binNumber):
    
    #turn into histogram data
    count, binEdges = np.histogram(
        distribution,
        bins=binNumber,
        range=(0,4),#np.min([3,np.max(distribution)])),
        )
    binWidth = binEdges[2] - binEdges[1]
    pdf = count/(len(distribution)*binWidth)
    binCenters = binEdges[1:] - binWidth/2
    
    #perform the curve fitting
    popt, pcov = curve_fit(
        lognormal,
        binCenters,
        pdf,
        p0=[1,1], 
        maxfev=10000,
        )
    
    #extract values
    mu = popt[0]
    sigma = popt[1]
    
    return binCenters, pdf, mu, sigma