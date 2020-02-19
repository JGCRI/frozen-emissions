"""
Diagnostic functions for frozen Emissions Factors (EFs) and frozen final emissions.
The functions from this file can be imported and executed elsewhere or invoked from
the command line.

Matt Nicholson
17 Feb 2020
"""
import sys
import os
import argparse
import pandas as pd
import numpy as np

# Insert src directory to Python path for importing
# sys.path.insert(1, '../src')
sys.path.append('..')

import utils
import ceds_io


def init_diag_parser():
    """
    Initialize a new argparse parser
    
    Parameters
    -----------
    None
    
    Return
    -------
    argparse.ArgumentParser object
    
    Args
    -----
    --frozen : str
        Path of the frozen CMIP6 Emissions Factors (EF) file
    --control : str
        Path of the unmodified control CMIP6 Emissions Factors (EF) file
        
    Example usage
    --------------
    $ python diagnostics.py --frozen /path/to/frozen_ef.csv --control /path/to/control_ef.csv
    $ python diagnostics.py --frozen /path/to/frozen_ef.csv --control /path/to/control_ef.csv --year 1950
    $ python diagnostics.py --frozen /path/to/frozen_ef.csv --control /path/to/control_ef.csv --year 'X1950'
    """
    parse_desc = """Diagnostics to compare frozen EFs to the original CMIP6 EFs"""
    
    parser = argparse.ArgumentParser(description=parse_desc)
    
    parser.add_argument('--frozen', metavar='frozen_ef', dest='frozen_ef',
                        required=True, action='store', type=str,
                        help='Path of the frozen CMIP6 EF file')
                        
    parser.add_argument('--control', metavar='control_ef', dest='control_ef',
                        required=True, action='store', type=str,
                        help='Path of the control (unmodified) CMIP6 EF file')
    
    parser.add_argument('--year', metavar='freeze_year', dest='freeze_year',
                        required=False, action='store', type=str, default='X1970',
                        help='Year at which the CMIP6 emissions factors were frozen')
                        
    return parser


def compare_emissions_factors(frozen_ef_path, control_ef_path, year='X1970'):
    """
    Compare the values of frozen emissions factors with those from a control
    emissions factor file. Quantifies how much the outlier removal as part of 
    the EF freezing process impacts EFs
    
    Parameters
    -----------
    frozen_ef_path : str
        Path of the frozen emissions factors file to read.
    control_ef_path : str
        Path of the control emissions factors file to read.
    year : int or str, optional
        Year at which the emissions factors were frozen. Default is 'X1970',
        the string representation of the CMIP6 emissions factors column name 
        representing the year 1970.
    """
    subset_cols = ['iso', 'sector', 'fuel', '']
    if (not isinstance(year, str) or year[0] != 'X'):
        year = 'X{}'.format(year)
    subset_cols[3] = year
    
    control_df = pd.read_csv(control_ef_path, sep=',', header=0)
    frozen_df  = pd.read_csv(frozen_ef_path, sep=',', header=0)
    
    # Extract a subset of the control & frozen EF dataframes containing only 
    # the columns 'iso', 'sector', 'fuel', and 'X<year>' since we only want to
    # compare the frozen and control EFs for <year> 
    control_df = control_df[subset_cols]
    frozen_df  = frozen_df[subset_cols]
    
    # Create a copy of the frozen dataframe that we can write diagnostic values to
    summary_df = frozen_df.copy()
    p_change = _calc_percent_change(np.asarray(control_df[year]), np.asarray(frozen_df[year]))
    summary_df[year] = p_change
    
    master_pchange_df = summary_df.copy()
    master_pchange_df = master_pchange_df.rename(columns={year: '{}-pchange'.format(year)})
    master_pchange_df['{}-frozen'.format(year)] = frozen_df[year]
    master_pchange_df['{}-cmip6'.format(year)]  = control_df[year]
    
    # Write the summary dataframe to the output/diagnostics directory
    species = _parse_species_from_path(frozen_ef_path)
    _write_pchange_master_csv(master_pchange_df, species)
    del master_pchange_df
    
    # Calculate stats for percentage change by sector
    sector_summary_df = _group_df(summary_df, 'sector', year)
    _write_pchange_sector_csv(sector_summary_df, species)
    del sector_summary_df
    
    # Calculate stats for percentage change by iso
    iso_summary_df = _group_df(summary_df, 'iso', year)
    _write_pchange_iso_csv(iso_summary_df, species)
    del iso_summary_df
    
    # Calculate stats for percentage change by fuel
    fuel_summary_df = _group_df(summary_df, 'fuel', year)
    _write_pchange_fuel_csv(fuel_summary_df, species)
    del fuel_summary_df
    
# ============================= Helper Functions ===============================

def _group_df(ef_df, kywrd, year):
    """
    Group an emissions factor dataframe and calculate the minimum, mean, and average
    emissions factors percentage change for frozen emissions factors.
    
    Parameters
    -----------
    ef_df : Pandas DataFrame
        Emissions Factors dataFrame containing only the columns ['iso', 'sector', 'fuel', 'X<year>'].
    kywrd : str
        Determines how to group the dataframe
    year : str
        Year at which the EFs were frozen, in CMIP6 csv column header format
        Ex: 'X1970'
    
    Return
    -------
    Pandas DataFrame
    """
    cols = {'min' : '{}-min'.format(year),
            'mean': '{}-mean'.format(year),
            'max' : '{}-max'.format(year)}
            
    drop_cols = {'sector': ['iso', 'fuel'],
                 'iso'   : ['sector', 'fuel'],
                 'fuel'  : ['iso', 'sector']}
                 
    if (kywrd not in drop_cols.keys()):
        raise ValueError('Invalid keyword arg. Only "iso", "sector", & "fuel" are valid')
    # Drop the columns appropriate for the given keyword arg
    grouped_df = ef_df.drop(drop_cols[kywrd], axis=1).copy()
    # Group the DataFrame rows by kywrd
    grouped_df = grouped_df.groupby([kywrd], as_index=False)
    # Calculate the min EF percentage change
    min_df  = grouped_df.min()
    min_df  = min_df.rename(columns={year: cols['min']})
    # Calculate the mean EF percentage change (p-change)
    mean_df = grouped_df.mean()
    mean_df = mean_df.rename(columns={year: cols['mean']})
    # Add the column of mean EF p-change values to the min EF p-change dataframe
    merged_df = min_df.merge(mean_df, on=kywrd)
    # Calculate the max EF percentage change
    max_df  = grouped_df.max()
    max_df  = max_df.rename(columns={year: cols['max']})
    # Add the column of max EF p-change values to the dataframe containing 
    # min & mean EF p-change values
    merged_df = merged_df.merge(max_df, on=kywrd)
    return merged_df
    

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
    
    
def _parse_species_from_path(ef_path):
    """
    Given the path of an EF file, get the corresponding emission species
    
    Parameters
    -----------
    ef_path : str   
        Path of an EF file
        
    Return
    -------
    str : Species corresponding to the EF file whose path was given as a parameter
    """
    f_name = os.path.basename(ef_path)
    species = ceds_io.get_species_from_fname(f_name)
    return species
    
    
def _write_pchange_csv(pchange_df, csv_path, verbose=True):
    """
    Write a dataframe containing EF values percentage change to .csv
    
    Parameters
    -----------
    df : Pandas DataFrame
        DataFrame containing the percentage change values
    csv_path : str
        Path of the file to write to
    """
    if (verbose):
        print('Frozen EF percent change data written to {}'.format(csv_path))
    pchange_df.to_csv(csv_path, sep=',', header=True, index=False)


def _write_pchange_master_csv(pchange_df, species, verbose=True):
    """
    Write the dataframe containing all EF percentage change values to .csv.
    Calls _write_pchange_csv() to do the actual file I/O.
    
    Parameters
    -----------
    pchange_df : Pandas DataFrame
        DataFrame containing the percentage change values
    species : str
        Name of the emission species corresponding to the dataframe
        
    Return
    -------
    str : path of the output .csv file
    """
    f_name = '{}_frozen_ef_pchange_master.csv'.format(species)
    csv_path = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', f_name)
    _write_pchange_csv(pchange_df, csv_path, verbose=verbose)
    return csv_path
    
    
def _write_pchange_sector_csv(pchange_df, species, verbose=True):
    """
    Write the dataframe containing all EF percentage change values grouped by 
    sector to .csv. Calls _write_pchange_csv() to do the actual file I/O.
    
    Parameters
    -----------
    pchange_df : Pandas DataFrame
        DataFrame containing the percentage change values
    species : str
        Name of the emission species corresponding to the dataframe
        
    Return
    -------
    str : path of the output .csv file
    """
    f_name = '{}_frozen_ef_pchange_sector.csv'.format(species)
    csv_path = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', f_name)
    _write_pchange_csv(pchange_df, csv_path, verbose=verbose)
    return csv_path
    
    
def _write_pchange_iso_csv(pchange_df, species, verbose=True):
    """
    Write the dataframe containing all EF percentage change values grouped by 
    ISO to .csv. Calls _write_pchange_csv() to do the actual file I/O.
    
    Parameters
    -----------
    pchange_df : Pandas DataFrame
        DataFrame containing the percentage change values
    species : str
        Name of the emission species corresponding to the dataframe
        
    Return
    -------
    str : path of the output .csv file
    """
    f_name = '{}_frozen_ef_pchange_iso.csv'.format(species)
    csv_path = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', f_name)
    _write_pchange_csv(pchange_df, csv_path, verbose=verbose)
    return csv_path
    
    
def _write_pchange_fuel_csv(pchange_df, species, verbose=True):
    """
    Write the dataframe containing all EF percentage change values grouped by 
    fuel to .csv. Calls _write_pchange_csv() to do the actual file I/O.
    
    Parameters
    -----------
    pchange_df : Pandas DataFrame
        DataFrame containing the percentage change values
    species : str
        Name of the emission species corresponding to the dataframe
        
    Return
    -------
    str : path of the output .csv file
    """
    f_name = '{}_frozen_ef_pchange_fuel.csv'.format(species)
    csv_path = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', f_name)
    _write_pchange_csv(pchange_df, csv_path, verbose=verbose)
    return csv_path
    
# ================================== Main ======================================

if (__name__ == '__main__'):
    parser = init_diag_parser()
    args = parser.parse_args()
    compare_emissions_factors(args.frozen_ef, args.control_ef)
