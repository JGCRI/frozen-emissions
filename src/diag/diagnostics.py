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
sys.path.insert(1, '../src')

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
    """
    parse_desc = """Diagnostics to compare frozen EFs to the original CMIP6 EFs"""
    
    parser = argparse.ArgumentParser(description=parse_desc)
    
    parser.add_argument('--frozen', metavar='frozen_ef', dest='frozen_ef',
                        required=True, action='store', type=str,
                        help='Path of the frozen CMIP6 EF file')
                        
    parser.add_argument('--control', metavar='control_ef', dest='control_ef',
                        required=True, action='store', type=str,
                        help='Path of the control (unmodified) CMIP6 EF file')
    return parser


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
    species = _parse_species_from_path(frozen_ef_path)
    _write_pchange_csv(summary_df, species)
    
    # Calculate stats for percentage change by sector
    sector_df = summary_df.drop(['iso', 'fuel'], axis=1).copy()
    sector_df = sector_df.groupby(['sector']).min()
    sector_df = sector_df.rename(columns={year: '{}-min'.format(year)})
    sector_df['{}-mean'.format(year)] = summary_df.groupby(['sector']).mean()
    sector_df['{}-max'.format(year)] = summary_df.groupby(['sector']).max()
    _write_pchange_sector_csv(sector_df, species)
    
    # Calculate stats for percentage change by iso
    iso_df = summary_df.drop(['sector', 'fuel'], axis=1).copy()
    iso_df = iso_df.groupby(['iso']).min()
    iso_df = iso_df.rename(columns={year: '{}-min'.format(year)})
    iso_df['{}-mean'.format(year)] = summary_df.groupby(['iso']).mean()
    iso_df['{}-max'.format(year)] = summary_df.groupby(['iso']).max()
    _write_pchange_iso_csv(iso_df, species)
    
    # Calculate stats for percentage change by fuel
    fuel_df = summary_df.drop(['iso', 'sector'], axis=1).copy()
    fuel_df = fuel_df.groupby(['fuel']).min()
    fuel_df = fuel_df.rename(columns={year: '{}-min'.format(year)})
    fuel_df['{}-mean'.format(year)] = summary_df.groupby(['fuel']).mean()
    fuel_df['{}-max'.format(year)] = summary_df.groupby(['fuel']).max()
    _write_pchange_fuel_csv(fuel_df, species)
    
    
# ============================= Helper Functions ===============================


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
    
    
def _write_pchange_csv(df, csv_path, verbose=True):
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
        print('Frozen EF percent change data written to {}'.format(f_path))
    pchange_df.to_csv(f_path, sep=',', header=True, index=False)


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
    f_path = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', f_name)
    _write_pchange_csv(df, csv_path, verbose=verbose)
    return f_path
    
    
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
    f_path = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', f_name)
    _write_pchange_csv(df, csv_path, verbose=verbose)
    return f_path
    
    
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
    f_path = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', f_name)
    _write_pchange_csv(df, csv_path, verbose=verbose)
    return f_path
    
    
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
    f_path = os.path.join(utils.get_root_dir(), 'output', 'diagnostic', f_name)
    _write_pchange_csv(df, csv_path, verbose=verbose)
    return f_path
    
# ================================== Main ======================================

if (__name__ == '__main__'):
    parser = init_diag_parser()
    args = parser.parse_args()
    compare_emissions_factors(args.frozen_ef, args.control_ef)
