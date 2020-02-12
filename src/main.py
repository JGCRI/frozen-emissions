"""
Main script that produces the frozen emissions

Matt Nicholson
7 Feb 2020
"""
# import logging
import argparse
import logging
import os
import pandas as pd

import log_config
import ceds_io
import config
import efsubset
import z_stats
import emission_factor_file

def init_parser():
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
    Freeze emissions factors for years >= 'year'
    
    'Freezing' the emissions factors means setting the values for years > a given
    year equal to their value for that year. For example, freezing emissions factors
    at 1970 means the emissions factors for years 1971-present are set to their
    1970 value
    
    Parameters
    -----------
    None, uses global CONFIG object
    
    Return
    -------
    None
    """
     # Unpack config directory paths for better readability
    data_path = config.CONFIG.dirs['cmip6']
    out_path = config.CONFIG.dirs['inter_out']
    
    main_log = logging.getLogger("main")
    main_log.info("In main::freeze_emissions()")
    main_log.info("data_path = {}".format(data_path))
    main_log.info("year = {}\n".format(config.CONFIG.freeze_year))
    
    # Get all Emission Factor filenames in the directory
    ef_files = ceds_io.fetch_ef_files(data_path)
        
    # Construct the column header strings for years >= 'year' param
    year_strs = ['X{}'.format(yr) for yr in range(config.CONFIG.freeze_year,
                                                  config.CONFIG.ceds_meta['year_last'] + 1)]
    
    # Begin for-loop over each species EF file
    for f_name in ef_files:
        
        species = ceds_io.get_species_from_fname(f_name)
        main_log.info("Processing species: {}".format(species))
        
        f_path = os.path.join(data_path, f_name)
        
        main_log.info("Loading EF DataFrame from {}".format(f_path))
        # ef_df = ceds_io.read_ef_file(f_path)
        ef_obj = emission_factor_file.EmissionFactorFile(species, f_path)
        
        # Get combustion sectors
        sectors = ef_obj.get_sectors()
        fuels = ef_obj.get_fuels()
        
        for sector in sectors:
            
            for fuel in fuels:
                
                main_log.info("--- Processing {}...{}...{}---".format(species, sector, fuel))
                
                print("Processing {}...{}...{}...".format(species, sector, fuel))
                
                if (ef_obj.get_comb_shape()[0] != 0):
                    # Calculate the median of the EF values
                    ef_median = z_stats.get_ef_median(ef_obj)
                    main_log.debug("EF data array median: {}".format(ef_median))
                    main_log.debug("Identifying outliers")
                    
                    outliers = z_stats.get_outliers_zscore(ef_obj, sector, fuel)
                    if (len(outliers) != 0):
                        main_log.debug("Setting outlier values to median EF value")
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
                        main_log.debug("No outliers were identified")
                    # Overwrite the current EFs for years >= 1970
                    main_log.debug("Overwriting original EF DataFrame with new EF values")
                else:
                    main_log.warning("Subsetted EF dataframe is empty")
            # --- End fuel loop ---
        # --- End sector loop ---
        # Freeze the combustion emissions
        main_log.debug("Freezing emissions...")
        ef_obj.freeze_emissions(year_strs)
        
        # Overwrite the corresponding values from the original EF DataFrame
        main_log.debug("Reconstructing total emissions factors DataFrame...")
        ef_obj.reconstruct_emissions()
        
        f_out = os.path.join(out_path, f_name)
        
        main_log.debug("Writing resulting {} DataFrame to file".format(species))
        print('Writing final {} DataFrame to: {}\n'.format(species, f_out))
        ef_obj.all_factors.to_csv(f_out, sep=',', header=True, index=False)
        main_log.info("DataFrame written to {}\n".format(f_out))
        
    # --- End EF file for-loop ---
    main_log.info("Finished processing all species\nLeaving main::freeze_emissions()\n")
    
    
def calc_emissions():
    """
    Calculate the hypothetical emissions from the frozen emissions and the CMIP6
    activity files
    
    Emissions = EF x Activity
    
    Parameters
    -----------
    None, uses global CONFIG object
        
    Return
    -------
    None, writes to file
    """
    logger = logging.getLogger("main")
    logger.info('In main::calc_emissions()')
    
    # Unpack for better readability
    dir_inter_out = config.CONFIG.dirs['inter_out']
    dir_cmip6 = config.CONFIG.dirs['cmip6']
    
    logger.debug('Searing for available species in {}'.format(dir_inter_out))
    
    em_species = ceds_io.get_avail_species(dir_inter_out)
    
    logger.debug('Emission species found: {}\n'.format(len(em_species)))
    
    # Create list of strings representing year column headers
    data_col_headers = ['X{}'.format(i) for i in range(config.CONFIG.ceds_meta['year_first'],
                                                       config.CONFIG.ceds_meta['year_last'])]
    
    for species in em_species:
        info_str = '\nCalculating frozen total emissions for {}...'.format(species)
        logger.debug(info_str)
        print(info_str)
        
        # Get emission factor file for species
        logger.debug('Fetching emission factor file from {}'.format(dir_inter_out))
        frozen_ef_file = ceds_io.get_file_for_species(dir_inter_out, species, "ef")
        
        # Get activity file for species
        logger.debug('Fetching activity file from {}'.format(dir_cmip6))
        try:
            activity_file = ceds_io.get_file_for_species(dir_cmip6, species, "activity")
        except:
            err_msg = 'No activity file found for {}'.format(species)
            logger.error(err_msg)
            print(err_msg)
            continue
        
        ef_path = os.path.join(dir_inter_out, frozen_ef_file)
        act_path = os.path.join(dir_cmip6, activity_file)
        
        # Read emission factor & activity files into DataFrames
        logger.debug('Reading emission factor file from {}'.format(ef_path))
        ef_df = pd.read_csv(ef_path, sep=',', header=0)
        
        logger.debug('Reading activity file from {}'.format(act_path))
        act_df = pd.read_csv(act_path, sep=',', header=0)
        
        # Get the 'iso', 'sector', 'fuel', & 'units' columns
        meta_cols = ef_df.iloc[:, 0:4]
        
        # Sanity check
        if (meta_cols.equals(act_df.iloc[:, 0:4])):
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
        
        logger.info('Calculating total emissions')
        
        if (ef_subs.shape != act_subs.shape):
            # Error is arising where ef_subs.shape = (55212, 265) &
            # act_subs.shape = (54772, 265).
            # ValueError will be raised by pandas
            logger.error('ValueError: ef_subs & act_subs could not be broadcast together')
            logger.debug('ef_subs.shape {}'.format(ef_subs.shape))
            logger.debug('act_subs.shape {}'.format(act_subs.shape))
        
        emissions_df = pd.DataFrame(ef_subs.values * act_subs.values,
                                    columns=ef_subs.columns, index=ef_subs.index)
        
        # Insert the meta ('iso', 'sector', 'fuel', 'units') columns at the 
        # beginning of the DataFrame
        logger.debug('Concatinating meta_cols and emissions_df DataFrames along axis 1')
        emissions_df = pd.concat([meta_cols, emissions_df], axis=1)
       
        f_name = '{}_total_CEDS_emissions.csv'.format(species)
        
        f_out = os.path.join(dir_inter_out, f_name)
        
        info_str = 'Writing emissions DataFrame to {}'.format(f_out)
        logger.debug(info_str)
        print(info_str)
        
        emissions_df.to_csv(f_out, sep=',', header=True, index=False)
        logger.info('Finished calculating total emissions for {}'.format(species))
        
    # End species loop
    logger.info("Finished processing all species")
    logger.info('Leaving validate::calc_emissions()\n')
    

def main():
    # Create a new argument parser & parse the command line args 
    parser = init_parser()
    args = parser.parse_args()
    
    # Parse the input YAML file & initialize global CONFIG 'constant'
    config.CONFIG = config.ConfigObj(args.input_file)
    
    # Initialize a new main log
    logger = log_config.init_logger(config.CONFIG.dirs['logs'], "main", level='debug')
    logger.info('Input file {}'.format(args.input_file))
    
    # Execute the specified function(s)
    if (args.function == 'all'):
        freeze_emissions()
        calc_emissions()
    elif (args.function == 'freeze_emissions'):
        freeze_emissions()
    elif (args.function == 'calc_emissions'):
        calc_emissions()
    else:
        raise ValueError('Invalid function argument. Valid args are "freeze_emissions" and "calc_emissions"')
        


if __name__ == '__main__':
    main()