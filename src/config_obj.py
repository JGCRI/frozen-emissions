"""
A class to hold configuration information used by the frozen emission scripts

Matt Nicholson
7 Feb 2020
"""
import yaml
from sys import platform
from os.path import basename

class ConfigObj:
    
    def __init__(self, yaml_path):
        """
        Constructor for a Config instance
        
        Parameters
        -----------
        yaml_path : str
            Path to the YAML input file to parse
            
        Attributes
        -----------
        ceds_meta : dict of {str : int}
            Dictionary containing CEDS metadata. 
            Keys: 
                year_first : First year of CEDS output
                year_last  : Last (most current) year of CEDS output
        dirs : dict of {str : str}
            Dictionary containing various input and output directory paths
        freeze_year : int
            Freeze emission factors for years >= this year.
        freeze_isos : str or list of str
            Freeze emissions for these CEDS ISOs. Default is 'all'.
        freeze_species : str or list of str
            Emission species to freeze.
        init_file : str
            Name of the init .yml file
        """
        self.dirs           = self._init_dirs()
        self.freeze_year    = None
        self.freeze_isos    = None
        self.freeze_species = None
        self.init_file      = None
        self.ceds_meta      = {}
        self._parse_yaml(yaml_path)
    
    def _init_dirs(self):
        """
        Initialize the 'dirs' instance attr
        """
        dirs = {'cmip6'    : None,
                'inter_out': None,
                'proj_root': None,
                'input'    : None,
                'output'   : None,
                'logs'     : None,
                'init'     : None}
        self.dirs = dirs
        
    def _parse_yaml(self, yaml_path):
        """
        Read the input YAML file
        
        Params
        -------
        yaml_path : str
            Absolute path of the YAML file
        """
        with open(yaml_path, 'r') as in_stream:
            try:
                info = yaml.safe_load(in_stream)
            except yaml.YAMLError as e:
                print(e)
                
        # Determine whether to use Windows or Linux paths based off the OS executing
        # the script
        if (platform.startswith('win')):
            op_sys = 'win'
        elif (platform.startswith('linux')):
            op_sys = 'linux'
        else:
            raise ValueError('Only Windows and Linux systems are currently supported')
            
        self._init_dirs()      # Initialize the instance's directory dictionary
        self.dirs['cmip6']     = info['dirs'][op_sys]['cmip6_inter']
        self.dirs['inter_out'] = info['dirs'][op_sys]['root_inter']
        self.dirs['proj_root'] = info['dirs'][op_sys]['root_proj']
        self.dirs['input']     = info['dirs']['input']
        self.dirs['output']    = info['dirs']['output']
        self.dirs['logs']      = info['dirs']['logs']
        self.dirs['init']      = info['dirs']['init']
        self.freeze_year       = int(info['freeze']['year'])
        self.freeze_isos       = info['freeze']['isos']
        self.freeze_species    = info['freeze']['species']
        self.init_file         = basename(yaml_path)
        self.ceds_meta['year_first'] = info['ceds']['year_first']
        self.ceds_meta['year_last'] = info['ceds']['year_last']
        
        
    def __repr__(self):
        return "<ConfigObj object {}>".format(self.init_file)
       