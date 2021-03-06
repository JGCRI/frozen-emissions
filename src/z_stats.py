# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 08:43:19 2019

@author: nich980
"""

import numpy as np
import logging

from os.path import join
from scipy import stats

import warnings
warnings.filterwarnings("error")    # Treat RuntimeWarnings as error

import ceds_io



def write_stats(ef_df, species, year, f_paths):
    
    f_out_name = '{}.{}'.format(species, f_paths['f_out_name'])
    
    f_out_abs = join(f_paths['f_out_path'], f_out_name)
    
    with open(f_out_abs, 'w') as fh:
        fh.write('sector,fuel,mean,median,std,sum,min_ef,max_ef')
        fh.write('\n')

    fuels = ef_df['fuel'].unique().tolist()
    sectors = ef_df['sector'].unique().tolist()
    
    for sector in sectors:
        ef_df_sector = ef_df[ef_df['sector'] == sector]
        
        for fuel in fuels:
            ef_df_fuel = ef_df_sector[ef_df_sector['fuel'] == fuel]
            
            ef_df_subs = ef_df_fuel['X{}'.format(year)]
   
            ef_mean = ef_df_subs.mean()
            ef_median = ef_df_subs.median()
            ef_std = ef_df_subs.std()
            ef_sum = ef_df_subs.sum()
            ef_min = ef_df_subs.min()
            ef_max = ef_df_subs.max()
           
            curr_str = '{},{},{},{},{},{},{},{}'.format(sector, fuel, ef_mean,
                                                        ef_median, ef_std, ef_sum,
                                                        ef_min, ef_max)
           
            with open(f_out_abs, 'a') as fh:
                fh.write(curr_str)
                fh.write('\n')


def get_ef_median(ef_obj):
    """
    Get the median of an array of EF values for the specified EF freeze year
    
    Parameters
    -----------
    ef_obj : EmissionFactorFile obj
    
    Return
    -------
    NumPy float 64
    """
    ef_list = ef_obj.get_factors_combustion()[ef_obj.freeze_year].tolist()
    med = np.median(ef_list)
    return med


def get_outliers_zscore(ef_obj, sector, fuel, thresh=3):
    """
    Identify outliers using their Z-Scores
    
    Parameters
    ----------
    ef_obj : EmissionFactorFile obj
    thresh : int, optional
        Absolute value of the Z-score threshold used to identify outliers
        
    Returns
    -------
    outliers : list of tuple - (str, float, float)
        ISOs and their respective EFs & z-scores that have been identified as outliers
    """
    logger = logging.getLogger('main')
    logger.debug("Calculating Z-scores...")
    iso_list = ef_obj.get_isos(unique=False)
    ef_df = ef_obj.get_factors_combustion()
    ef_df = ef_df.loc[(ef_df['sector'] == sector) & (ef_df['fuel'] == fuel)]
    ef_list = ef_df[ef_obj.freeze_year].tolist()
    ef_list = np.asarray(ef_list, dtype=np.float64)
    outliers = []
    # If we have an array of all zeros, do nothing
    if (not np.all(ef_list == 0.0)):
        try:
            score = np.abs(stats.zscore(ef_list))
            bad_z = np.where(score > thresh)[0]
        except RuntimeWarning:
            logger.error("RuntimeWarning caught while calculating z-score. Returning empty outlier array")
        else:
            for z_idx in bad_z:
                outliers.append((iso_list[z_idx], ef_list[z_idx], z_idx))
            logger.debug("Outliers identified: {}".format(len(outliers)))
    else:
        logger.debug("EF data array is all zeros. Returning empty outlier array")
    return outliers


def get_outliers_std(efsubset_obj):
    """
    Identify outliers using the Standard Deviation Method
    
    All values that fall outside of 3 standard deviations of the mean data value
    will be flagged as outliers
    
    Parameters
    ----------
    efsubset_obj : EFSubset object
        
    Returns
    -------
    outliers : list of tuple - (str, float)
        ISOs and their respective EFs that have been identified as outliers
    """
    logger = logging.getLogger('main')
    logger.info("Idenfitying outliers using Standard Deviation method...")
    
    outliers = []
    
    ef_std = np.std(efsubset_obj.ef_data)
    ef_mean = np.mean(efsubset_obj.ef_data)
    cutoff = ef_std * 3
    
    limit_lower = ef_mean - cutoff
    limit_upper = ef_mean + cutoff
    
    for idx, ef in enumerate(efsubset_obj.ef_data):
        if ((ef > limit_upper) or (ef < limit_lower)):
            outliers.append((efsubset_obj.isos[idx], ef))
            
    logger.debug("Outliers identified: {}".format(len(outliers)))
    
    return outliers


def get_outliers_iqr(efsubset_obj, outlier_const=1.5):
    """
    IQR method from 
    https://www.dasca.org/world-of-big-data/article/identifying-and-removing-outliers-using-python-packages
    
    Parameters
    ----------
    efsubset_obj : EFSubset object
        
    Returns
    -------
    outliers : list of tuple - (str, float)
        ISOs and their respective EFs that have been identified as outliers
    """
    logger = logging.getLogger('main')
    logger.info("Calculating IQR...")
    
    outliers = []
    
    upper_quartile = np.percentile(efsubset_obj.ef_data, 75)
    lower_quartile = np.percentile(efsubset_obj.ef_data, 25)
    
#    print("Lower quartile: {}".format(lower_quartile))
#    print("Upper quartile: {}".format(upper_quartile))
    
    IQR = (upper_quartile - lower_quartile) * outlier_const

    upper_limit = upper_quartile + IQR
    lower_limit = lower_quartile - IQR
    
    for idx, ef in enumerate(efsubset_obj.ef_data):
        if (ef > upper_limit or ef < lower_limit):
            outliers.append((efsubset_obj.isos[idx], ef, idx))
            
    logger.debug("Outliers identified: {}".format(len(outliers)))
    
    return outliers


def get_boxcox(efsubset_obj):
    """
    Parameters
    ----------
    efsubset_obj : EFSubset object
    
    Return
    ------
    xt : ndarray
        Box-Cox power transformed array
    lam : float
        The lambda that maximizes the log-likelihood function
    """
    logger = logging.getLogger('main')
    logger.info("Performing Box Cox transform...")
    
    data = np.asarray(efsubset_obj.ef_data, dtype=np.float64)
    
    # If the data values are tiny, scale the values to avoid overflow 
    # during numpy arithmetic
    data_med = np.median(data)
    if (data_med < 1.0e-4):
        scale_factor = 1.0e3
        data = data * scale_factor
        logger.debug("Median of data array < 1.0e-4. Scaling by {}".format(data_med, scale_factor))
    
    try:
        xt, lam = stats.boxcox(data)
        logger.debug("Box Cox transform successful")
    except ValueError:
        # ValueError: Data must be positive
        # Temporarily discarding the 0, and then using -1/λ for the transformed value of 0
        logger.info("Data values <= 0 encountered")
        
        pos_data = data[data > 0]
        
        try:
            x, lam = stats.boxcox(pos_data)
        except ValueError:
            # Occurs when all data values are 0, hence pos_data is empty
            # Return data as xt as theres nothing we can do
            xt = data
            lam = 0
            logger.debug("Data values are all 0. Returning original data array")
        else:
            xt = np.empty_like(data)
            
            xt[data > 0] = x
            xt[data == 0] = -1/lam
            
            logger.debug("Box Cox transform successful")
    
    return (xt, lam)
    

def plot_df(efsubset_obj, plt_opts):
    """
    Make a scatter plot of an EF dataframe
    
    Parameters
    -----------
    ef_df : Pandas DataFrame
        DataFrame containing data from an emission factors file
    sector : str
        CEDS emisions sector to subset
    fuel : str
        CEDS fuel to subset
    year : int
        The year who's EFs we wish to subset
    species : str
        Emissions species who's EF data is represented in the EF DataFrame
    plt_opts : dict
        Plotting options 
    """
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    x = [i for i in range(len(efsubset_obj.isos))]
    y = efsubset_obj.ef_data
    
    ax.scatter(x, y, s=8)
    
    if (plt_opts['plot_outliers'] == True):
        outliers = get_outliers_zscore(efsubset_obj, thresh=plt_opts['z_thresh'])
#        import copy
#        boxcox, lam = get_boxcox(efsubset_obj)
#        ef_obj_boxcox = copy.deepcopy(efsubset_obj)
#        ef_obj_boxcox.ef_data = boxcox
#        outliers = get_outliers_zscore(ef_obj_boxcox, thresh=plt_opts['z_thresh'])
        
        x_out = [i[2] for i in outliers]
        y_out = [j[1] for j in outliers]
#        y_out = [y[i] for i in x_out]
        
        ax.scatter(x_out, y_out, marker="x", color="r", s=16)
    
    font_size = 10
    
    plt.title("Emission Factor for {} - {}".format(efsubset_obj.year, efsubset_obj.species),
              loc='left', fontsize=font_size)
    
    plt.title("Sector: {}, Fuel: {}".format(efsubset_obj.sector, efsubset_obj.fuel),
              loc='right', fontsize=font_size)
    
#    plt.axis([0, len(efsubset_obj.isos), 0, 2])
    plt.axis([0, len(efsubset_obj.isos), 0, 1])
    
    plt.xlabel("ISO")
    plt.ylabel("Emission Factor")
    plt.tight_layout()

    if (plt_opts['show'] == True):
        plt.show()
        
    if (plt_opts['save']):
        f_name = "{}.{}.{}.png".format(efsubset_obj.species, efsubset_obj.sector, efsubset_obj.fuel)
        f_path = join(plt_opts['out_path_abs'], f_name)
        plt.savefig(f_path, dpi=300)
    
    plt.close()
       
