"""
This file holds variables and whatnot for use in tests

Matt Nicholson
12 Feb 2020
"""
import logging
import os

def nuke_logs(target, log_dir):
    """
    Remove any existing logs from the logs/ subdirectory
    
    Parameters
    -----------
    target : str
        Target log file to delete
    log_dir : str
        Path to the log directory
    """
    if (not target.endswith('.log')):
        target = target + '.log'
    try:
        os.remove(os.path.join(log_dir, target))
    except FileNotFoundError as err:
        pass
# ------------------------------------------------------------------------------

def init_test_log(log_name, level='debug'):
    """
    Initialize a new log for the test file
    
    Parameters
    -----------
    log_name : str 
        Log file name. Also the name of the test file calling the function.
    level : str, optional
        Logging level. Default is 'debug'.
        
    Return
    -------
    logging.Logger object
    """
    log_dir = 'logs'
    log_levels = {'debug': logging.DEBUG,
                  'info' : logging.INFO,
                  'warn' : logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL
                  }
    
    nuke_logs(log_name, log_dir)
    
    if (not os.path.isdir(log_dir)):
        os.mkdir(log_dir)
    
    if (not log_name.endswith('.log')):
        f_name = '{}.log'.format(log_name)
    log_path = os.path.join(log_dir, f_name)
    
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    
    handler = logging.FileHandler(log_path)
    handler.setFormatter(log_format)
        
    logger = logging.getLogger(log_name)
    logger.setLevel(log_levels[level])
    logger.addHandler(handler)
    logger.info("Log created!\n")
    
    return logger
# ------------------------------------------------------------------------------

def subset_df(ef_df, iso):
    df = ef_df.loc[(ef_df['iso'] == iso) &
                   (ef_df['sector'].isin(expected_sectors))]
    return df
# ------------------------------------------------------------------------------

def subset_noncombust_sectors(df):
        """
        Return a subset of an EF dataframe that contains only non-combustion
        sectors
        
        Parameters
        -----------
        df : Pandas DataFrame
        
        Return
        -------
        Pandas DataFrame
        """
        subset_df = df.loc[df['sector'].isin(non_combustion_sectors)].copy()
        return subset_df
# ------------------------------------------------------------------------------

def subset_combust_sectors(df):
        """
        Return a subset of an EF dataframe that contains only combustion sectors
        
        Parameters
        -----------
        df : Pandas DataFrame
        
        Return
        -------
        Pandas DataFrame
        """
        subset_df = df.loc[df['sector'].isin(expected_sectors)].copy()
        return subset_df
# ------------------------------------------------------------------------------
    
def subset_iso(df, isos):
    """
    Return a subset of an EF dataframe that contains only EFs for a given ISO
    or list of ISOs
    
    Parameters
    -----------
    df : Pandas DataFrame
    isos : str or list of str
        ISO or ISOs to subset
    
    Return
    -------
    Pandas DataFrame
    """
    if (not isinstance(isos, list)):
        isos = [iso]
    subset_df = df.loc[df['iso'].isin(isos)].copy()
    return subset_df
# ------------------------------------------------------------------------------

def subset_iso_inverse(df, isos):
    """
    Return a subset of an EF dataframe that contains only EFs for ISO(s) that
    are not present in 'isos'
    
    Parameters
    -----------
    df : Pandas DataFrame
    isos : str or list of str
        ISO or ISOs to subset
    
    Return
    -------
    Pandas DataFrame
    """
    if (not isinstance(isos, list)):
        isos = [iso]
    inv_isos = [x for x in expected_isos if x not in isos]
    subset_df = df.loc[df['iso'].isin(inv_isos)].copy()
    return subset_df
# ------------------------------------------------------------------------------
    
def get_year_headers(year_start, year_end, mode='incl'):
    """
    Generate a list of CMIP6/CEDS emissions factors file year columns headers
    Ex: 'X1970'
    
    Parameters
    ----------
    year_start : int
        First year in the sequence
    year_end : int
        Last year in the sequence
    mode : str, optional
        Determines whether or not to include the ending year in the header list.
        mode == 'incl', which means year_end *will* be included in the list.
        mode == 'excl' means year_end *will not* be included in the list.
        Default is 'incl'.
        
    Return
    -------
    list of str
    """
    # Upper bound is year_end + 1 due to how range() handles upper bounds
    try:
        if (mode == 'incl'):
            year_end += 1
        headers = ['X{}'.format(year) for year in range(year_start, year_end)]
    except TypeError as err:
        # year_start and/or year_end has been given as a str instead of int.
        # Cast them as ints and make a recusrive call
        year_start = int(year_start)
        year_end   = int(year_end)
        headers = get_year_headers(year_start, year_end, mode=mode)
    return headers
    
# ==============================================================================
# ================================= Constants ==================================
# ==============================================================================

# CMIP6/CEDS combustion-related sectors ----------------------------------------
expected_sectors = sorted(
    ['1A1a_Electricity-public', '1A1a_Electricity-autoproducer',
     '1A1a_Heat-production', '1A2a_Ind-Comb-Iron-steel', '1A2b_Ind-Comb-Non-ferrous-metals',
     '1A2c_Ind-Comb-Chemicals', '1A2d_Ind-Comb-Pulp-paper', '1A2e_Ind-Comb-Food-tobacco',
     '1A2f_Ind-Comb-Non-metalic-minerals', '1A2g_Ind-Comb-Construction',
     '1A2g_Ind-Comb-transpequip', '1A2g_Ind-Comb-machinery', '1A2g_Ind-Comb-mining-quarying',
     '1A2g_Ind-Comb-wood-products', '1A2g_Ind-Comb-textile-leather', '1A2g_Ind-Comb-other',
     '1A3ai_International-aviation', '1A3aii_Domestic-aviation', '1A3b_Road',
     '1A3c_Rail', '1A3di_International-shipping', '1A3dii_Domestic-navigation',
     '1A3eii_Other-transp', '1A4a_Commercial-institutional', '1A4b_Residential',
     '1A4c_Agriculture-forestry-fishing', '1A5_Other-unspecified']
    )
            
# CMIP6/CEDS fuels -------------------------------------------------------------         
expected_fuels = sorted(
    ['biomass', 'brown_coal', 'coal_coke', 'diesel_oil',
     'hard_coal', 'heavy_oil', 'light_oil', 'natural_gas']
    )

# CMIP6/CEDS ISOs --------------------------------------------------------------                  
expected_isos = sorted(
    ['abw', 'afg', 'ago', 'alb', 'are', 'arg', 'arm', 'asm',
     'atg', 'aus', 'aut', 'aze', 'bdi', 'bel', 'ben', 'bfa', 'bgd', 'bgr',
     'bhr', 'bhs', 'bih', 'blr', 'blz', 'bmu', 'bol', 'bra', 'brb', 'brn',
     'btn', 'bwa', 'caf', 'can', 'che', 'chl', 'chn', 'civ', 'cmr', 'cod',
     'cog', 'cok', 'col', 'com', 'cpv', 'cri', 'cub', 'cuw', 'cym', 'cyp',
     'cze', 'deu', 'dji', 'dma', 'dnk', 'dom', 'dza', 'ecu', 'egy', 'eri',
     'esh', 'esp', 'est', 'eth', 'fin', 'fji', 'flk', 'fra', 'fro', 'fsm',
     'gab', 'gbr', 'geo', 'gha', 'gib', 'gin', 'global', 'glp', 'gmb', 'gnb',
     'gnq', 'grc', 'grd', 'grl', 'gtm', 'guf', 'gum', 'guy', 'hkg', 'hnd',
     'hrv', 'hti', 'hun', 'idn', 'ind', 'irl', 'irn', 'irq', 'isl', 'isr',
     'ita', 'jam', 'jor', 'jpn', 'kaz', 'ken', 'kgz', 'khm', 'kir', 'kna',
     'kor', 'kwt', 'lao', 'lbn', 'lbr', 'lby', 'lca', 'lie', 'lka', 'lso',
     'ltu', 'lux', 'lva', 'mac', 'mar', 'mda', 'mdg', 'mdv', 'mex', 'mhl',
     'mkd', 'mli', 'mlt', 'mmr', 'mne', 'mng', 'moz', 'mrt', 'msr', 'mtq',
     'mus', 'mwi', 'mys', 'nam', 'ncl', 'ner', 'nga', 'nic', 'niu', 'nld',
     'nor', 'npl', 'nzl', 'omn', 'pak', 'pan', 'per', 'phl', 'plw', 'png',
     'pol', 'pri', 'prk', 'prt', 'pry', 'pse', 'pyf', 'qat', 'reu', 'rou',
     'rus', 'rwa', 'sau', 'sdn', 'sen', 'sgp', 'slb', 'sle', 'slv', 'som',
     'spm', 'srb', 'srb (kosovo)', 'ssd', 'stp', 'sur', 'svk', 'svn', 'swe',
     'swz', 'sxm', 'syc', 'syr', 'tca', 'tcd', 'tgo', 'tha', 'tjk', 'tkl',
     'tkm', 'tls', 'ton', 'tto', 'tun', 'tur', 'twn', 'tza', 'uga', 'ukr',
     'ury', 'usa', 'uzb', 'vct', 'ven', 'vgb', 'vir', 'vnm', 'vut', 'wlf',
     'wsm', 'yem', 'zaf', 'zmb', 'zwe']
    )
    
# Non-combustion sectors -------------------------------------------------------
non_combustion_sectors = sorted(
    ['1A1bc_Other-transformation', '1A1bc_Other-feedstocks', '1B1_Fugitive-solid-fuels',
     '1B2_Fugitive-petr-and-gas', '1B2d_Fugitive-other-energy', '2A1_Cement-production',
     '2A2_Lime-production', '2A6_Other-minerals', '2B_Chemical-industry', '2C_Metal-production',
     '2D_Degreasing-Cleaning', '2D3_Other-product-use', '2D_Paint-application',
     '2D3_Chemical-products-manufacture-processing', '2H_Pulp-and-paper-food-beverage-wood',
     '2L_Other-process-emissions', '3B_Manure-management', '3D_Soil-emissions',
     '3I_Agriculture-other', '3D_Rice-Cultivation', '3E_Enteric-fermentation',
     '3F_Agricultural-residue-burning-on-fields', '5A_Solid-waste-disposal',
     '5E_Other-waste-handling', '5C_Waste-incineration', '6A_Other-in-total',
     '5D_Wastewater-handling', '6B_Other-not-in-total', '7A_Fossil-fuel-fires',
     '11A_Volcanoes', '11B_Forest-fires', '11C_Other-natural']
    )
