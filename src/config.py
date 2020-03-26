"""
A class to hold configuration information used by the frozen emission scripts

Matt Nicholson
7 Feb 2020
"""
import yaml
import os
from sys import platform

# Global config 'constant'
CONFIG = None

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
            Keys:
                'root'  : Path to root project directory
                'input' : Path to main input directory
                'output': Path to main output directory
                'cmip6' : Path to CMIP6/intermediate-output directory
                'ceds'  : Path to local CEDS project direcotyr
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
        # Get the project root, which will be one level up
        project_root, _ = os.path.split(os.path.dirname(os.path.abspath(__file__)))
        dirs = {'root': project_root,
                'cmip6'  : None,
                'input'  : None,
                'output' : None,
                'ceds'   : None}
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
        # self.dirs['cmip6']  = info['dirs'][op_sys]['cmip6']
        self.dirs['ceds']   = info['dirs'][op_sys]['ceds']
        self.dirs['input']  = os.path.join(self.dirs['root'], 'input')
        self.dirs['output'] = os.path.join(self.dirs['root'], 'output')
        self.dirs['cmip6']  = os.path.join(self.dirs['input'], 'cmip6')
        self.freeze_year    = int(info['freeze']['year'])
        try:     # Is freeze_isos a string?
            self.freeze_isos = info['freeze']['isos'].lower()
        except:  # We have determined that freeze_isos is not a string
            self.freeze_isos = [x.lower() for x in info['freeze']['isos']]
        self.freeze_species  = info['freeze']['species']
        self.init_file       = os.path.basename(yaml_path)
        self.ceds_meta['year_first'] = info['ceds']['year_first']
        self.ceds_meta['year_last'] = info['ceds']['year_last']
        
        
    def __repr__(self):
        return "<ConfigObj object {}>".format(self.init_file)
       