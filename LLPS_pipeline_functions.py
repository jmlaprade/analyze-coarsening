# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 09:48:05 2021

@author: Jeremy Laprade
         jeremymlaprade@gmail.com
"""


# ----------------------------------------------------------------------------
# get input files information (probability maps)
# ----------------------------------------------------------------------------
def get_files(file_dir):
    from os import listdir
    path = file_dir+'Probabilities\\'
    #input('Enter path to folder containing data: ')
    images = listdir(path)
    return path, images
    
# ----------------------------------------------------------------------------
# calcualte probability quality (certainty) maps and values
# ----------------------------------------------------------------------------
def analyze_threshold(raw_data, file_dir, prob_th, dt, t0):
    import numpy as np
    from os import makedirs
    import imageio
    from skimage import io
    import matplotlib.pyplot as plt
    
    #read the data from file
    uncert_dir = file_dir + 'Threshold Uncertainty\\'
    makedirs(
            uncert_dir,
            exist_ok=True,
            )
    
    n_files = len(raw_data[1])
    droplet_uncertainty = np.zeros(n_files)
    total_uncertainty = np.zeros(n_files)  
    for i in range(n_files):
        #import probability map from file
        prob_map = io.imread(
                raw_data[0]+raw_data[1][i],
                )
        
        #calculate full uncertainty map from probability
        uncertainty_map = 1 - 2*abs(prob_map - 0.5)
        imageio.imwrite(
                uncert_dir+'uncertainty_'+str(i)+'.tif', 
                uncertainty_map,
                )
        
        droplet_uncertainty[i] = np.mean(
                1 - 2*abs(prob_map[prob_map >= prob_th] - 0.5),
                )
        total_uncertainty[i] = np.mean(
                1 - 2*abs(prob_map - 0.5),
                )
    time = dt*(np.array((range(n_files)))) - t0
    
    plt.figure()
    plt.plot(time, droplet_uncertainty, label='Droplets only')
    plt.plot(time, total_uncertainty, label='Total image')
    plt.legend()
    plt.xlabel('Time, $t$ (s)')
    plt.ylabel('Uncertainty, $\delta$P')
    plt.savefig(file_dir+'uncertainty.png')
    plt.close()
# ----------------------------------------------------------------------------
# calcualte coarsening over time from probability maps
# ----------------------------------------------------------------------------
def analyze_data(raw_data, file_dir, prob_th, dt, t0, conv2):
    import numpy as np
    from os import makedirs
    import imageio
    from skimage import io
    from skimage.measure import label, regionprops

    #create required directories for saving data
    binary_dir = file_dir + 'Binaries\\'
    makedirs(
            binary_dir,
            exist_ok=True,
            )
    results_dir = file_dir + 'Results\\'
    makedirs(
            results_dir,
            exist_ok=True,
            )
    makedirs(
            results_dir+'\\Distributions\\',
            exist_ok=True,
            )
    #prepare needed arrays for storage
    n_files = len(raw_data[1])
    N = np.zeros(n_files)
    avg_R = np.zeros(n_files)
    V_tot = np.zeros(n_files)    
    
    for i in range(n_files):
        #import probability map from file
        prob_map = io.imread(
                raw_data[0]+raw_data[1][i],
                )
        #create binary image from probabiliy map
        binary_raw = np.uint32(1*(prob_map >= prob_th))
        imageio.imwrite(
                binary_dir+'binary_'+str(i)+'.tif', 
                binary_raw,
                )
        
        #label objects and measure them
        binary_labeled = label(binary_raw)
        props = regionprops(
                binary_labeled,
                cache = 'False', #slightly improves computation time
                )

        #extract measured values of interest
        area_raw = np.array([r.area for r in props])
        area = (conv2)*area_raw[area_raw > 4]
        R = np.sqrt(area/np.pi)
        V = (4*np.pi/3)*R**3
        V_tot = np.sum(V)
        N = len(R)
        avg_R = np.mean(R)
        
        #write distribution to a text file
        np.savetxt(
                results_dir+'Distributions\\radii_'+str(i)+'.txt', 
                R,
                fmt = '%1.3f'
                )

        #append results in text file
        dataLog = open(
                results_dir+'results.txt', 'a'
                )
        dataLog.write(
            str(dt*(i+1)) + ' , ' + str(avg_R) + ' , '
            + str(N) + ' , ' + str(V_tot) + '\n')
        dataLog.close()

# ----------------------------------------------------------------------------
# curve fitting functions for analysis
# ----------------------------------------------------------------------------

def lognormal_fit(x, sigma, mu, scale):
    import numpy as np
    preFactor = scale*(x*sigma*np.sqrt(2*np.pi))**-1
    numerator = (np.log(x)-mu)**2
    denominator = 2*sigma**2
    return preFactor*np.exp(-numerator/denominator)

# ----------------------------------------------------------------------------
# plotting coarsening results from text files
# ----------------------------------------------------------------------------
def plot_results(result_path, dt, t0, dist_inspect):
    import numpy as np
    import matplotlib.pyplot as plt
    from os import makedirs
    from scipy.optimize import curve_fit
    
    plot_path = result_path + 'Plots\\'
    makedirs(
        plot_path,
        exist_ok=True,
        )

    ind_array = (dist_inspect/dt)   
    for i in ind_array:
        dist = np.loadtxt(
                result_path+'Distributions\\radii_'+str(int(i))+'.txt', 
                )

        #determine histogram counts for radius distribution
        probCounts, binEdges = np.histogram(
            dist, 
            int(np.floor(np.sqrt(len(dist)))),
            )
        binCent = binEdges[1:] - (binEdges[1]-binEdges[0])/2
        
        #fit the distribution to a log-normal function
        popt, pcov = curve_fit(
            lognormal_fit,
            binCent,
            probCounts/len(dist),
            )
        
        #plot radius distribution (with log-normal fit?)
        plt.figure()
        plt.plot(
            binCent,
            probCounts/len(dist),
            'k.',
            label='Measured distribution',
            ) 
        plt.plot(
            binCent,
            lognormal_fit(
                binCent, 
                popt[0], 
                popt[1], 
                popt[2]
                ),
            'r-',
            label='Log-normal fit',
            )
        plt.xlabel('Droplet radius, $r$ ($\mu$m)')        
        plt.ylabel('Probability, $P(r)$')
        plt.title('Droplet radius distribution, $t = $'+str(dt*i)+'s')
        plt.savefig(plot_path+'distribution_'+str(dt*i)+'.png')
        plt.close()

    #load in data for droplet dynamics
    data = np.loadtxt(
        result_path+'results.txt', 
        delimiter = ',',
        )
    
    #plot average radius over time in loglog scale
    plt.figure()
    plt.loglog(
        data[:,0],
        data[:,1],
        'k.',
        )                                          
    plt.xlabel('Time, $t$ (s)')
    plt.ylabel('average radius, $< R >$ ($\mu$m)')
    plt.savefig(plot_path+'avg_radius.png')
    plt.close()
    
    #plot number over time in loglog scale
    plt.figure()
    plt.loglog(
        data[:,0],
        data[:,2],
        )                                          
    plt.xlabel('Time, $t$ (s)')
    plt.ylabel('Number of droplets, $N$')
    plt.savefig(plot_path+'number.png')
    plt.close()
    
    #plot total droplet volume over time
    plt.figure()
    plt.plot(
        data[:,0],
        data[:,3],
        )                                          
    plt.xlabel('Time, $t$ (s)')
    plt.ylabel('Total droplet volume, $V_{tot}$ ($\mu$m$^{3}$)')
    plt.ticklabel_format(
        axis = 'y',
        style = 'sci',
        scilimits=(0,0),
        )
    plt.savefig(plot_path+'total_droplet_volume.png')
    plt.close()
