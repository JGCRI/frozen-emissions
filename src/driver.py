"""
This file contains the functions that freeze emissions factors and produce 
frozen total emissions files.

Usage
-----
python driver.py <config_file> <options>

Matt Nicholson
7 Feb 2020
"""
import argparse
import logging
import os
import pandas as pd

import log_config
import ceds_io
import config
import z_stats
import emission_factor_file


def init_parser():
    """
    Initialize a new argparse parser.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    argparse.ArgumentParser object
    
    Args
    -----
    input_file; str
        Path of the input YAML file. This argument is required.
    -f, --function; str, optional
        Function (out of "freeze_emissions" & "calc_emissions") to execute.
        Default is to execute both functions. 
        Example: Recalculate final emissions only
            > python main.py path/to/yaml -f "calc_emissions"
    """
    parse_desc = """Freeze CEDS CMIP6 emissions factors and calculate frozen total emissions"""
    
    parser = argparse.ArgumentParser(description=parse_desc)
    
    parser.add_argument(metavar='input_file', dest='input_file',
                        action='store', type=str,
                        help='Path of the input YAML file')
                        
    parser.add_argument('-f', '--function', metavar='function', required=False,
                        dest='function', action='store', type=str, default='all',
                        help=('Optional; Function(s) to execute ("freeze_emissions" or "calc_emissions").'
                              'Default value is "both", which executes both functions'))
    return parser


def freeze_emissions():
    """
    Freeze CMIP6 emissions factors for years >= 'year'.
    
    'Freezing' the emissions factors means setting the values for years > a given
    year equal to their value for that year. For example, freezing emissions factors
    at 1970 means the emissions factors for years 1971-present are set to their
    1970 value.
    
    Parameters
    ----------
    None, uses global CONFIG object
    
    Input files
    -----------
    CMIP6 emissions factors
        Located in /input/cmip.
        Filename format: H.<species>_total_EFs_extended.csv
    
    Returns
    -------
    None, writes frozen emissions factors files to /output directory.
    """
    failed_species = [''] * len(config.CONFIG.freeze_species)
    fail_idx = 0
    
    # Unpack config directory paths for better readability
    dir_cmip6 = config.CONFIG.dirs['cmip6']
    dir_output = config.CONFIG.dirs['output']
    
    logger = logging.getLogger("main")
    logger.info("In main::freeze_emissions()")
    logger.info("dir_cmip6 = {}".format(dir_cmip6))
    logger.info("freeze year = {}".format(config.CONFIG.freeze_year))
        
    # Construct the column header strings for years >= 'year' param
    year_strs = ['X{}'.format(yr) for yr in range(config.CONFIG.freeze_year,
                                                  config.CONFIG.ceds_meta['year_last'] + 1)]
                                                  
    logger.debug("year_strs[0] = {}".format(year_strs[0]))
    logger.debug("year_strs[-1] = {}".format(year_strs[-1]))
    
    # Begin for-loop over each species we want to freeze
    for species in config.CONFIG.freeze_species:
        logger.info("Processing species: {}".format(species))
        
        # Get the species' EF file
        try:
            f_path = ceds_io.get_file_for_species(dir_cmip6, species, "ef")
        except FileNotFoundError as err:
            # If a FileNotFoundError is returned, log it and move on to the next species
            err_str = "Error encountered while fetching EF file: {}".format(err)
            logger.error(err_str)
            failed_species[fail_idx] = species
            fail_idx += 1
            continue

        logger.info("Loading EF DataFrame from {}".format(f_path))
        # ef_df = ceds_io.read_ef_file(f_path)
        ef_obj = emission_factor_file.EmissionFactorFile(species, f_path)
        
        # Get combustion sectors
        sectors = ef_obj.get_sectors()
        fuels = ef_obj.get_fuels()
        
        # Not going to python-ize these nested loops as it decreases readability
        for sector in sectors:
            for fuel in fuels:
                info_str = "Processing {}...{}...{}".format(species, sector, fuel)
                logger.info("--- {} ---".format(info_str))
                print("{}...".format(info_str))
                
                if (ef_obj.get_comb_shape()[0] != 0):
                    # Calculate the median of the EF values
                    ef_median = z_stats.get_ef_median(ef_obj)
                    logger.debug("EF data array median: {}".format(ef_median))
                    logger.debug("Identifying outliers")
                    
                    outliers = z_stats.get_outliers_zscore(ef_obj, sector, fuel)
                    if (len(outliers) != 0):
                        logger.debug("Setting outlier values to median EF value")
                        # Set the EF value of each idenfitied outlier to the median of the EF values
                        for olr in outliers:
                            # Set outlier values to the calculated median val
                            ef_obj.combustion_factors.loc[
                                    (ef_obj.combustion_factors['iso'] == olr[0]) &
                                    (ef_obj.combustion_factors['sector'] == sector) &
                                    (ef_obj.combustion_factors['fuel'] == fuel) &
                                    (ef_obj.combustion_factors[ef_obj.freeze_year] == olr[1])
                                    ] = ef_median
                    else:
                        logger.debug("No outliers were identified")
                    # Overwrite the current EFs for years >= 1970
                    logger.debug("Overwriting original EF DataFrame with new EF values")
                else:
                    logger.warning("Subsetted EF dataframe is empty")
            # --- END fuel loop -----
        # --- END sector loop -----
        # Freeze the combustion emissions
        logger.debug("Freezing emissions...")
        ef_obj.freeze_emissions(year_strs)
        
        # Overwrite the corresponding values from the original EF DataFrame
        logger.debug("Reconstructing total emissions factors DataFrame...")
        ef_obj.reconstruct_emissions()
        
        f_name = os.path.basename(f_path)
        f_out = os.path.join(dir_output, f_name)
        
        info_str = "Writing frozen emissions factors DataFrame to {}".format(f_out)
        logger.debug(info_str)
        print(info_str + '\n')
        
        ef_obj.all_factors.to_csv(f_out, sep=',', header=True, index=False)
        logger.info("--- Finished processing {} ---\n".format(species))
    # --- END EF file loop -----
    for failure in failed_species:
        if failure != '':
            logger.warning('Emissions calculation failed for {}'.format(failure))
    logger.info("Finished processing all species\nLeaving main::freeze_emissions()\n")
    
    
def calc_emissions():
    """
    Produce frozen total emissions files using frozen emission emissions factors
    produced by freeze_emissions() and CMIP6 activity files. Frozen total emissions
    files are written to the output/ directory.
    
    Emissions = EF x Activity
    
    Parameters
    ----------
    None, uses global CONFIG object.
    
    Input files
    -----------
    Frozen emissions factors
        Located in /output.
        Filename format: H.<species>_total_EFs_extended.csv
    CMIP6 species activity
        Located in /input/cmip.
        Filename format: H.<species>_total_activity_extended.csv
        
    Returns
    -------
    None, writes frozen total emissions files to /output directory.
    """
    failed_species = [''] * len(config.CONFIG.freeze_species)
    fail_idx = 0
    
    logger = logging.getLogger("main")
    logger.info('In main::calc_emissions()')
    
    # Unpack for better readability
    dir_output = config.CONFIG.dirs['output']
    dir_cmip6 = config.CONFIG.dirs['cmip6']
    
    # Create list of strings representing year column headers
    data_col_headers = ['X{}'.format(i) for i in range(config.CONFIG.ceds_meta['year_first'],
                                                       config.CONFIG.ceds_meta['year_last'] + 1)]
    logger.debug('data_col_headers[0] = '.format(data_col_headers[0]))
    logger.debug('data_col_headers[-1] = '.format(data_col_headers[-1]))
    
    for species in config.CONFIG.freeze_species:
        info_str = '\nCalculating frozen total emissions for {}...'.format(species)
        logger.info(info_str)
        print(info_str)
        
        # Get emission factor file for species
        try:
            frozen_ef_file = ceds_io.get_file_for_species(dir_output, species, "ef")
        except FileNotFoundError as err:
            # If a FileNotFoundError is returned, log it and move on to the next species
            err_str = "Error encountered while fetching EF file: {}".format(err)
            logger.error(err_str)
            failed_species[fail_idx] = species
            fail_idx += 1
            print(err_str)
            continue
        
        # Get activity file for species
        try:
            activity_file = ceds_io.get_file_for_species(dir_cmip6, species, "activity")
        except:
            # If a FileNotFoundError is returned, log it and move on to the next species
            err_msg = 'No activity file found for {}'.format(species)
            logger.error(err_msg)
            failed_species[fail_idx] = species
            fail_idx += 1
            print(err_msg)
            continue
        
        # Read emission factor & activity files into DataFrames
        logger.debug('Reading emission factor file from {}'.format(frozen_ef_file))
        ef_df = pd.read_csv(frozen_ef_file, sep=',', header=0)
        
        logger.debug('Reading activity file from {}'.format(activity_file))
        act_df = pd.read_csv(activity_file, sep=',', header=0)
        
        # Get the 'iso', 'sector', & 'fuel' columns
        meta_cols = ef_df.iloc[:, 0:4]
        
        # Sanity check
        if (not ef_df.iloc[:, 0:3].equals(act_df.iloc[:, 0:3])):
            err_str = 'Emission Factor & Activity DataFrames have mis-matched meta columns'
            logger.error(err_str)
            raise ValueError(err_str)
        
        # Get a subset of the emission factor & activity files that contain numerical
        # data so we can compute emissions. We *could* skip this step and just
        # do the slicing whithin the dataframe multiplication step (~line 245),
        # but that is much messier and confusing to read
        logger.debug('Subsetting emission factor & activity DataFrames')
        ef_subs = ef_df[data_col_headers]
        act_subs = act_df[data_col_headers]
        
        logger.debug('ef_subs.shape {}'.format(ef_subs.shape))
        logger.debug('act_subs.shape {}'.format(act_subs.shape))
        
        logger.debug('Calculating total emissions')
        
        if (ef_subs.shape != act_subs.shape):
            # Error is arising where ef_subs.shape = (55212, 265) &
            # act_subs.shape = (54772, 265).
            # ValueError will be raised by pandas
            logger.error('ValueError: ef_subs & act_subs could not be broadcast together')
        
        emissions_df = pd.DataFrame(ef_subs.values * act_subs.values,
                                    columns=ef_subs.columns, index=ef_subs.index)
        
        # Insert the meta ('iso', 'sector', 'fuel', 'units') columns at the 
        # beginning of the DataFrame
        logger.debug('Concatinating meta_cols and emissions_df DataFrames along axis 1')
        emissions_df = pd.concat([meta_cols, emissions_df], axis=1)
        
        if (species == 'SO2' or species == 'CO2'):
            # Correct for mass-balance correction by copying pre-1970 emissions
            # directly from the CMIP6 total emissions file
            cols = ['X{}'.format(yr) for yr in range(config.CONFIG.ceds_meta['year_first'], 1971)]
            cmip_file = os.path.join(dir_cmip6, 'final-emissions', 'SO2_total_CEDS_emissions.csv')
            logger.debug('Reading SO2 CMIP6 total emissions file from {}'.format(cmip_file))
            cmip_df = pd.read_csv(cmip_file, sep=',', header=0)
            cmip_so2 = cmip_df.loc[cmip_df['sector'] == '1A1bc_Other-transformation'].copy()
            # Extract 1750-1970 emissions
            cmip_so2 = cmip_so2[cols]
            # Update the values of 1750-1970 emissions for the 1A1bc_Other-transformation
            # sector in the master final emissions dataframe
            emissions_df.update(cmip_so2)
            
        # Correct missing tanker loading sector or else gridding fails due to versioning.
        logger.debug('Adding missing global 1A3di_Oil_Tanker_Loading sector')
        zeros = [0] * len(data_col_headers)
        tls_row = ['global', '1A3di_Oil_Tanker_Loading',  'process', 'kt'] + zeros
        tls_df = pd.DataFrame([tls_row], columns=emissions_df.columns.values.tolist())
        emissions_df = emissions_df.append(tls_df, ignore_index=True)
        
        f_name = '{}_total_CEDS_emissions.csv'.format(species)
        f_out = os.path.join(dir_output, f_name)
        
        info_str = 'Writing emissions DataFrame to {}'.format(f_out)
        logger.debug(info_str)
        print(info_str + '\n')
        
        emissions_df.to_csv(f_out, sep=',', header=True, index=False)
        logger.info('Finished calculating total emissions for {}'.format(species))
    # --- End species loop ---
    for failure in failed_species:
        if failure != '':
            logger.warning('Emissions calculation failed for {}'.format(failure))
    logger.info('Finished processing all species! Leaving validate::calc_emissions()\n')


def main():
    # Create a new argument parser & parse the command line args 
    parser = init_parser()
    args = parser.parse_args()
    
    # Parse the input YAML file & initialize global CONFIG 'constant'
    config.CONFIG = config.ConfigObj(args.input_file)
    
    # Initialize a new main log
    logger = log_config.init_logger('logs', 'main', level='debug')
    logger.info('Input file {}'.format(args.input_file))
    
    info_str = 'Function(s) to execute: {}'
    # Execute the specified function(s)
    if (args.function == 'all'):
        logger.info(info_str.format('freeze_emissions() & calc_emissions()'))
        freeze_emissions()
        calc_emissions()
    elif (args.function == 'freeze_emissions'):
        logger.info(info_str.format('freeze_emissions()'))
        freeze_emissions()
    elif (args.function == 'calc_emissions'):
        logger.info(info_str.format('calc_emissions()'))
        calc_emissions()
    else:
        raise ValueError('Invalid function argument. Valid args are "all", "freeze_emissions", or "calc_emissions"')
        

if __name__ == '__main__':
    main()
