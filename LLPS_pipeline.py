# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 09:36:45 2021

@author: Jeremy Laprade
         jeremymlaprade@gmail.com
"""

#import imageio
#from os import makedirs

import numpy as np
from LLPS_pipeline_functions import ( 
        get_files,
        analyze_threshold,
        analyze_data,
        plot_results
        )

# ----------------------------------------------------------------------------
# user input prompts for analysis options
# ----------------------------------------------------------------------------
prob_analysis = int(input('Do analysis of probability threshold results?: '))
coarsening_analysis = int(input('Do analysis of coarsening?: '))
if coarsening_analysis == 1:
    plt_results = int(input('Plot and save results automatically?: '))
    
# ----------------------------------------------------------------------------
# global constants and global parameters
# ----------------------------------------------------------------------------

#input real-world parameters
px = 6.5
obj = 15
dt = 5*10
t0 = -300
dist_inspect = np.array((100, 300, 1000, 3000))
px_conv = px/obj
px_conv2 = px_conv*px_conv

prob_th = 0.5

file_dir = 'E:\\2D Active Nematics\\LLPS\\' \
    '21-12-10_14uMatp_10uMns_15x_5sInt_Ti2-Ham_68F_1\\Illastik\\'
raw_data = get_files(file_dir)

"""
binary_dir = file_dir+'Binaries\\'
makedirs(
    binary_dir,
    exist_ok=True,
    )
"""

# ----------------------------------------------------------------------------
# main analysis functions
# ----------------------------------------------------------------------------

#run analysis on quality of probability maps
if prob_analysis == 1:
    analyze_threshold(raw_data, file_dir, prob_th, dt, t0)
elif prob_analysis == 0:
    print('Probability analysis skipped!')
else:
    print('Probability analysis request must be either 1 \
          (for yes) or 0 (for no)')


#run analysis on binarized probability maps to measure coarsening
if coarsening_analysis == 1:
    analyze_data(raw_data, file_dir, prob_th, dt, t0, px_conv2)
elif prob_analysis == 0:
    print('Coarsening analysis skipped!')
else:
    print('Coarsening analysis request must be either 1 \
          (for yes) or 0 (for no)')

if coarsening_analysis == 1:
    #plot results from coarsening if analyzed
    if plt_results == 1:
        plot_results(file_dir + 'Results\\', dt, abs(t0), dist_inspect)
    elif plt_results == 0:
        print('Coarsening analysis skipped!')

