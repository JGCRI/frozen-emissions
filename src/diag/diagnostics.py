"""
Diagnostic functions for frozen Emissions Factors (EFs) and frozen final emissions

Matt Nicholson
17 Feb 2020
"""
import sys
import os
import pandas as pd
import numpy as np

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import utils

def compare_emissions_factors(frozen_ef_path, control_ef_path, year):
    """
    Compare the values of frozen emissions factors with those from a control
    emissions factor file. Quantifies how much the outlier removal as part of 
    the EF freezing process impacts EFs
    
    Parameters
    -----------
    frozen_ef_path : str
        Path of the frozen emissions factors file to read
    control_ef_path : str
        Path of the control emissions factors file to read
    """
    col_names = ['iso', 'sector', 'fuel', '']
    if (not isinstance(year, str) or year[0] != 'X'):
        year = 'X{}'.format(year)
    col_names[3] = year
    
    control_df = pd.read_csv(control_ef_path, sep=',', header=0)
    frozen_df  = pd.read_csv(frozen_ef_path, sep=',', header=0)
    
    # Subset for the given year
    control_df = control_df[col_names]
    frozen_df  = frozen_df[col_names]
    
    # Create a copy of the frozen dataframe that we can write diagnostic values to
    summary_df = frozen_df.copy()
    p_change = _calc_percent_change(np.asarray(control_df[year]), np.asarray(frozen_df[year]))
    summary_df[year] = p_change
    
    # Write the summary dataframe to the output/diagnostics directory
    summary_fname = 'frozen_ef_pchange.csv'
    summary_fpath = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', summary_fname)
    print('Frozen emission percent change data written to {}'.format(summary_fpath))
    summary_df.to_csv(summary_fpath, sep=',', header=True, index=False)
    
def _calc_percent_change(old_val, new_val):
    """
    Calculate the percentage change between an old value and a new value
    
    Parameters
    ----------
    old_val : int, float, list of int, list of float
    new_val : int, float, list of int, list of float
    
    Return
    ------
    float or list of float : Percentage change as a decimal number
    """
    delta_v = np.subtract(new_val, old_val)
    p_change = np.divide(delta_v, old_val)
    return p_change
    
    