"""
Python 3.6
emissions_factor_file.py

Class to represent a CMIP6 Emissions Factors (EF) File.

Instance Attributes
-------------------
species : str
    Name of the emission species represented in the EF file.
path : str  
    Path of the EF file being processed.
all_factors : Pandas DataFrame
    DataFrame containing the entirety of the EF file.
combustion_factors : Pandas DataFrame
    DataFrame containing only emissions factors from combustion-related sectors.
freeze_year : str
    Year at which to freeze the EFs, formatted to match the format of 
    the EF dataframe year column headers (ex: 'X1970').
    
Class Methods
-------------
__init__()
    Constructor. Initializes a new EmissionFactorFile instance.
get_species()
    Return the emissions species represented in an EmissionFactorFile instance.
get_path()
    Return the path of the parent emissions factor file.
get_shape()
    Return the shape of the instance's dataframe containing all emissions factors.
get_comb_shape() 
    Return the shape of the instance's dataframe containing emissions factors 
    from combustion-related sectors only.
get_sectors()
    Return a list of unique sectors present in an EmissionFactorFile's master or
    combustion EF dataframe.
get_fuels()
    Return a list of uniquefuels present in an EmissionFactorFile's master or
    combustion EF dataframe.
get_factors_all()
    Return the instance's dataframe that contains all emissions factors,
    regardless of their sector. 
get_factors_combustion()
    Return the instance's dataframe that contains only emissions factors from 
    combustion-related sectors.
get_isos()
    Return a list of ISOs present in an instance's EF dataframe. Can access both
    the master EF and combustion EF dataframes.
freeze_emissions()
    Set all combustion-related EFs for years greater than the
    freeze year equal to their value at the freeze year.
reconstruct_emissions()
    Update the EF values in the original, unedited EF dataframe with their
    corresponding frozen EF values.
_filter_isos()
    Remove any ISOs from the combustion EF DataFrame that are not meant to be frozen.
_parse_file()
    Parse a CMIP6 emissions factor file.
_get_comb_factors()
    Get a subset of the emissions factors that are from combustion-related sectors.
_log_init()
    Write information about the newly-initialized EmissionFactorFile instance
    to the main log file.
_write_diagnostics()
    Write diagnostics files describing the ISOs and sectors of the EmissionFactorFile
    instance that are to be frozen.


Matt Nicholson
12 Feb 2020
"""
import logging
import os
import pandas as pd
import numpy as np

import config

logger = logging.getLogger('main')

class EmissionFactorFile:
    
    def __init__(self, species, f_path):
        """
        Constructor for an EmissionFactorFile instance.
        
        Parameters
        -----------
        species : str
            Emission species represented in the EF file.
        f_path : str
            Path of the EF file.
            
        Attributes
        -----------
        species : str
            Name of the emission species represented in the EF file.
        path : str  
            Path of the EF file being processed.
        all_factors : Pandas DataFrame
            DataFrame containing the entirety of the EF file.
        combustion_factors : Pandas DataFrame
            DataFrame containing only emissions factors from combustion-related sectors.
        freeze_year : str
            Year at which to freeze the EFs, formatted to match the format of 
            the EF dataframe year column headers (ex: 'X1970').
        """
        self.species     = species
        self.path        = f_path
        self.all_factors = self._parse_file(f_path)
        self.freeze_year = 'X{}'.format(config.CONFIG.freeze_year)
        self.combustion_factors = self._get_comb_factors()
        if (config.CONFIG.freeze_isos != 'all' and config.CONFIG.freeze_isos != ['all']):
            self._filter_isos()
        self._log_init()
        self._write_diagnostics()
    
    def get_species(self):
        """
        Return
        -------
        str : the instance's species
        """
        return self.species
    
    def get_path(self):
        """
        Return
        -------
        str : the instance's path
        """
        return self.path
    
    def get_shape(self):
        """
        Get the shape of an instance's dataframe that contains all emissions
        factors. 
        
        Return
        -------
        tuple of int
        """
        return self.all_factors.shape
        
    def get_comb_shape(self):
        """
        Get the shape of an instance's dataframe that contains emissions factors
        from combustion-related sectors only.
        
        Return
        -------
        tuple of int
        """
        return self.combustion_factors.shape
    
    def get_sectors(self, ef='comb'):
        """
        Get the sectors in the EF file.
        
        Parameters
        -----------
        ef : string
            If 'all', all sectors will be returned. If 'comb', only combustion-related
            sectors will be returned. Default is 'comb'
        
        Return
        -------
        List of str
        """
        if (ef != 'comb'):
            ret_val = self.all_factors['sector'].unique().tolist()
        else:
            ret_val = self.combustion_factors['sector'].unique().tolist()
        return ret_val
    
    def get_fuels(self, ef='comb'):
        """
        Get the fuels 
        
        Parameters
        -----------
        ef : string
            If 'all', all fuels will be returned. If 'comb', only combustion-related
            fuels will be returned. Default is 'comb'
        
        Return
        -------
        List of str
        """
        if (ef != 'comb'):
            ret_val = self.all_factors['fuel'].unique().tolist()
        else:
            ret_val = self.combustion_factors['fuel'].unique().tolist()
        return ret_val
    
    def get_factors_all(self):
        """
        Return the instance's dataframe that contains all emissions factors,
        regardless of their sector. 
        
        Return
        -------
        Pandas DataFrame
        """
        return self.all_factors
        
    def get_factors_combustion(self):
        """
        Return
        -------
        Pandas DataFrame : The instance's dataframe containing only emissions factors
        from combustion-related sectors
        """
        return self.combustion_factors
    
    def get_isos(self, ef='comb', unique=True):
        """
        Return a list of ISOs present in an instance's EF dataframe.
        
        Parameters
        -----------
        ef : str, optional
            Emissions factors to retrieve ISOs from. Options are:
                * 'comb': Only ISOs present in the combustion sector dataframe
                          will be returned
                * 'all' : All ISOs will be returned, regardless of what sector
                          they're associated with.
            Default is 'comb'.
        unique : bool, optional
            Specifies whether to return only unique ISOs or the entire list of 
            ISOs including duplicates. Default is True, meaning only unique ISOs
            will be returned. unique = False is useful when preserving the index
            of the ISOs is desired.
            
        Return
        -------
        list of str           
        """
        if (ef != 'comb'):
            if (unique):
                ret_val = self.all_factors['iso'].unique().tolist()
            else:
                ret_val = self.all_factors['iso'].tolist()
        else:
            if (unique):
                ret_val = self.combustion_factors['iso'].unique().tolist()
            else:
                ret_val = self.combustion_factors['iso'].tolist()
        return ret_val
        
    def freeze_emissions(self, year_strs):
        """
        Set all combustion-related emissions factors for years greater than the
        freeze year equal to their value at the freeze year.
        
        Parameters
        -----------
        year_strs : list of str
            List of strings representing years >= the freeze year, in column header
            format (ex: 'X1970').
            
        Return
        -------
        None.
        """
        year_0 = year_strs[0]
        for year in year_strs[1:]:
            self.combustion_factors[year] = self.combustion_factors[year_0]
            
    def reconstruct_emissions(self):
        """
        Update the EF values in the original, unedited EF dataframe with their
        corresponding frozen EF values. 
        
        Updates the values of the instance's 'all_factors' dataframe in-place.
        
        Parameters
        -----------
        None.
        
        Return
        -------
        None.
        """
        self.all_factors.update(self.combustion_factors)
    
    def _filter_isos(self):
        """
        Remove any ISOs from the combustion EF DataFrame that are not meant to be frozen.
        
        Parameters
        -----------
        None.
        
        Return
        -------
        None.
        """
        iso_list = config.CONFIG.freeze_isos
        logger.debug("Filtering ISOs for {}".format(iso_list))
        if (not isinstance(iso_list, list)):
            iso_list = [iso_list]
        self.combustion_factors = self.combustion_factors.loc[self.combustion_factors['iso'].isin(iso_list)].copy()
        
    def _parse_file(self, f_path):
        """
        Parse a CMIP6 EF file.
        
        Parameters
        -----------
        ef_path : str
            Path of the EF file to parse.
            
        Return
        -------
        Pandas DataFrame
        """
        logger.debug("Reading EF file {}".format(f_path))
        ef_df = pd.read_csv(f_path, sep=',', header=0)
        return ef_df
    
    def _get_comb_factors(self):
        """
        Get a subset of the emissions factors that are from combustion-related
        sectors. Filter if applicable.
        
        Parameters
        -----------
        None.
        
        Return
        -------
        Pandas DataFrame
        """
        combustion_sectors = ['1A1a_Electricity-public', '1A1a_Electricity-autoproducer',
                              '1A1a_Heat-production', '1A2a_Ind-Comb-Iron-steel',
                              '1A2b_Ind-Comb-Non-ferrous-metals', '1A2c_Ind-Comb-Chemicals',
                              '1A2d_Ind-Comb-Pulp-paper', '1A2e_Ind-Comb-Food-tobacco',
                              '1A2f_Ind-Comb-Non-metalic-minerals', '1A2g_Ind-Comb-Construction',
                              '1A2g_Ind-Comb-transpequip', '1A2g_Ind-Comb-machinery',
                              '1A2g_Ind-Comb-mining-quarying', '1A2g_Ind-Comb-wood-products',
                              '1A2g_Ind-Comb-textile-leather', '1A2g_Ind-Comb-other',
                              '1A3ai_International-aviation', '1A3aii_Domestic-aviation',
                              '1A3b_Road', '1A3c_Rail', '1A3di_International-shipping',
                              '1A3dii_Domestic-navigation', '1A3eii_Other-transp',
                              '1A4a_Commercial-institutional', '1A4b_Residential',
                              '1A4c_Agriculture-forestry-fishing', '1A5_Other-unspecified']
        combustion_df = self.all_factors.loc[self.all_factors['sector'].isin(combustion_sectors)].copy()
        return combustion_df
        
    def _log_init(self):
        """
        Log information about the newly-initialized EmissionFactorFile instance.
        
        Parameters
        ----------
        None.
            
        Returns
        -------
        None.
        """
        logger.debug('New EmissionFactorFile instance created for {}'.format(self.species))
        logger.debug('    Parent file....{}'.format(self.path))
        logger.debug('    Freeze year....{}'.format(self.freeze_year))
        logger.debug('    Comb DF shape: {}'.format(self.get_comb_shape()))
        logger.debug('    Comb Sectors...{}'.format(self.get_sectors()))
        logger.debug('    Comb ISOs......{}'.format(self.get_isos()))
        
    def _write_diagnostics(self):
        """
        Write some diagnostics files.
        
        Currently writes a CSV file containing the sectors and ISOs that are
        going to be frozen.
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        None.
        
        Output files
        ------------
        frozen_isos_sectors.csv
            CSV file containing ISOs and their respective sectors that are going
            to be frozen.
        """
        diag_fname = '{}_frozen_isos_sectors.csv'.format(self.species)
        out_dir = os.path.join(config.CONFIG.dirs['root'], 'src', 'diagnostics')
        if not os.path.isdir(out_dir):
            logger.debug('Creating diagnostic directory {}'.format(out_dir))
            os.mkdir(out_dir)
        diag_df = self.combustion_factors[['iso', 'sector', 'fuel']]
        logger.debug('Writing diagnostics file {}'.format(diag_fname))
        diag_df.to_csv(os.path.join(out_dir, diag_fname), sep=',', header=True, index=False)

    def __repr__(self):
        return "<EmissionFactorFile object - {} {}>".format(self.species, self.shape)
