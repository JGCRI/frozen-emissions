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
        self.shape = None
        self.species = species
        self.path = f_path
        self.isos = self._parse_isos(f_path)
    
    def get_species(self):
        return self.species
    
    def get_path(self):
        return self.path
    
    def get_shape(self):
        return self.shape
    
    def get_min_year(self):
        return self.isos.values()[0].columns.values.tolist()[0]
    
    def get_max_year(self):
        return self.isos.values()[0].columns.values.tolist()[0]
    
    def get_sectors(self):
        return self.isos.values()[0].get_sectors()
    
    def get_fuels(self):
        return self.isos.values()[0].get_fuels()
    
    def _filter_isos(self, iso_dict):
        """
        Remove any ISOs from the 'isos' dictionary that do not appear in the given
        'iso_list'
        
        Parameters
        -----------
        iso_list : list of str
            List of ISOs to keep
        
        Return
        -------
        Dict of {str : ISO obj}
        """
        iso_list = config.CONFIG.freeze_isos
        if (not isinstance(iso_list, list)):
            iso_list = [iso_list]
        ret_dict = {key: val for key, val in iso_dict.items() if key in iso_list}
        return ret_dict
    
    def _parse_isos(self, ef_path):
        """
        Parse a CMIP6 EF file and create a new ISO object for each
        ISO in the file
        
        Parameters
        -----------
        ef_path : str
            Path of the EF file to parse
            
        Return
        -------
        dict of {str : ISO obj}
            Dict where a key is the name of an iso and the value is the 
            ISO object corresponding to that ISO
        """
        ef_df = pd.read_csv(ef_path, sep=',', header=0)
        iso_dict = dict.fromkeys(ef_df['iso'].unique().tolist())
        self.shape = ef_df.shape
        for iso_name in iso_dict.keys():
            iso_dict[iso_name] = isos.ISO(iso_name, self.species, ef_df.loc[ef_df['iso'] == iso_name])
        if (config.CONFIG.freeze_isos != 'all' or config.CONFIG.freeze_isos != ['all']):
            iso_dict = self._filter_isos(iso_dict)
        return iso_dict
    
    def __repr__(self):
        return "<EmissionFactorFile object - {} {}".format(self.species, self.shape)
    
    