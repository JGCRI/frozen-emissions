"""
Class to represent a CMIP6 Emission Factor (EF) File

Matt Nicholson
12 Feb 2020
"""
import logging
import pandas as pd

import config
import isos

logger = logging.getLogger('main')

class EmissionFactorFile:
    
    def __init__(self, species, f_path):
        """
        Constructor for an EmissionFactorFile instance
        
        Parameters
        -----------
        species : str
            Emission species represented in the EF file
        f_path : str
            Path of the EF file
            
        Attributes
        -----------
        size : tuple of (int, int)
            Overall shape of the EF file
        species : str
            Name of the species represented in the EF file
        path : str  
            Path of the EF file corresponding to the instance
        isos : dict of {str : iso obj}
            Dict where a key is a str representation of an ISO name and the 
            corresponding value is an ISO object for that ISO
        """
        logger.debug('Creating EmissionFactorFile instance {} from {}'.format(species, f_path))
        self.species = species
        self.path = f_path
        self.all_factors = self._parse_file(f_path)
        self.combustion_factors = self._get_comb_factors()
        self.freeze_year = 'X{}'.format(config.CONFIG.freeze_year)
    
    def get_species(self):
        return self.species
    
    def get_path(self):
        return self.path
    
    def get_shape(self):
        return self.all_factors.shape
        
    def get_comb_shape(self):
        return self.combustion_factors.shape
    
    def get_sectors(self, ef='comb'):
        """
        Get the sectors in the EF file
        
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
        return self.all_factors
        
    def get_factors_combustion(self):
        return self.combustion_factors
    
    def get_isos(self, ef='comb', unique=True):
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
        year_0 = year_strs[0]
        for year in year_strs[1:]:
            self.combustion_factors[year] = self.combustion_factors[year_0]
            
    def reconstruct_emissions(self):
        self.all_factors.update(self.combustion_factors)
    
    def _filter_isos(self, ef_df):
        """
        Remove any ISOs from the combustion EF DataFrame that are not meant to be frozen
        
        Parameters
        -----------
        ef_df : Pandas DataFrame
            DataFrame or combuistion-related emissions factors to filter 
        
        Return
        -------
        Pandas DataFrame
        """
        iso_list = config.CONFIG.freeze_isos
        logger.debug("Filtering ISOs for {}".format(iso_list))
        if (not isinstance(iso_list, list)):
            iso_list = [iso_list]
        ret_val = self.combustion_factors.loc[elf.combustion_factors['iso'].isin(iso_list)]
        return ret_val
        
    def _parse_file(self, f_path):
        """
        Parse a CMIP6 EF file
        
        Parameters
        -----------
        ef_path : str
            Path of the EF file to parse
            
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
        sectors. Filter if applicable
        
        Parameters
        -----------
        None
        
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
        if (config.CONFIG.freeze_isos != 'all' and config.CONFIG.freeze_isos != ['all']):
            combustion_df = self._filter_isos(combustion_df)
        return combustion_df
    
    def __repr__(self):
        return "<EmissionFactorFile object - {} {}>".format(self.species, self.shape)
    
    