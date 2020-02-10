"""
Author: Matt Nicholson
31 Dec 19

This script reads the CEDS Master_Fuel_Sector_List.xlsx file into a Pandas DataFrame
and extracts a subset of the DataFrame for combustion sectors
"""
import pandas as pd
from os.path import join

import config

def create_csv():
    """
    Create a csv file containing CEDS combustion sectors
    
    Parameters
    -----------
    dirs : dict of str, str
        Dictionary holding paths needed for I/O
    
    Return
    ------
    Tuple of (str, DataFrame)
        Absolute path of the created csv and the subsetted combustion DataFrame
    """
    fname = "Master_Fuel_Sector_List.xlsx"
    f_out = "combustion_sectors.csv"

    # Path to Master_Fuel_Sector_List.xlsx from within the top-level CEDS directory
    file_dir = join("input", "mappings")

    # Construct absolute path to the file
    abs_path = join(CONFIG.dirs['ceds'], file_dir, fname)

    # Read the excel sheet into a DataFrame
    print("Reading {}".format(join("...", file_dir, fname)))
    df = pd.read_excel(abs_path, sheet_name="Sectors", header=0)

    # Get a subset of the DataFrame containing only combustion sectors
    df_comb = df.loc[df['type'] == 'comb']

    outpath = join(CONFIG.dirs['input'], f_out)

    print("Writing combustion sector csv to {}".format(outpath))
    df_comb.to_csv(outpath, sep=',', header=True, index=False)
    
    return (outpath, df_comb)
