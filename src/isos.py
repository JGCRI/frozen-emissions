"""
A class to represent a CMIP6 ISO

Matt Nicholson
12 Feb 2020
"""
import logging
import pandas as pd

import config

logger = logging.getLogger('main')

class ISO:
    
    def __init__(self, iso_name, species, iso_efs):
        """
        Constructor for an ISO instance
        
        Parameters
        -----------
        iso_name : str
            Name of the CMIP6 ISO
        iso_efs : Pandas DataFrame
            DataFrame containing emissions factors for all sectors and fuels
            associated with the ISO
        """
        logger.debug('Creating ISO instance {}'.format(iso_name))
        self.name = iso_name
        self.species = species
        self.emissions_factors = iso_efs
        self.shape = iso_efs.shape
        
    def get_combustion_sector_efs(self):
        """
        Get a subset of the ISO's sectors that are combustion-related
        
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
        combustion_df = self.emissions_factors.loc[self.emissions_factors['sector'].isin(combustion_sectors)]
        return combustion_df
    
    def get_sectors(self, mode='all'):
        """
        Get sectors present in the ISO's emission factor dataframe
        
        Parameters
        -----------
        mode : str, optional
            If mode == 'c', 'comb', or 'combustion', only combustion-related sectors
            will be returned. Default is 'all'.
        
        Return
        -------
        List of str
        """
        kwrd = ['c', 'comb', 'combustion']
        if (mode in kwrd):
            sectors = self.get_combustion_sector_efs()['sector'].tolist()
        else:
            sectors = self.emissions_factors['sector'].tolist()
        return sectors
    
    def get_fuels(self):
        """
        Get a list of unique fuels present in the ISO's EF dataframe
        
        Parameters
        -----------
        None
        
        Return
        -------
        List of str
        """
        fuels = self.emissions_factors['fuel'].unique().tolist()
        return fuels
    
    def get_name(self):
        """
        Get the name of the ISO
        
        Parameters
        -----------
        None
        
        Return
        -------
        str
        """
        return self.name
    
    def get_species(self):
        return self.species
        
    def __repr__(self):
        return "<ISO object - {} {}".format(self.name, self.species)