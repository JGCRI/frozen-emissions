"""
A class to hold configuration information used by the frozen emission scripts

Matt Nicholson
7 Feb 2020
"""
import yaml

def Class Config:
    
    def __init__(self, yaml_path):
        """
        Constructor for a Config instance
        
        Parameters
        -----------
        yaml_path : str
            Path to the YAML input file to parse
            
        Attributes
        -----------
        freeze_year : str or int
            Freeze emission factors for years >= this year.
        freeze_isos : str or list of str
            Freeze emissions for these CEDS ISOs. Default is 'all'.
        freeze_species : str or list of str
            Emission species to freeze.
        dir_cmip6_inter : str
            Path of the CMIP6 'intermediate-output' directory, which holds the 
            raw emission factor files.
        dir_root_inter : str
            Path of the project's 'intermediate-output' directory.
        input_file : str
            Name of the input file
        """
        self.freeze_year = None
        self.freeze_isos = None
        self.freeze_species = None
        self.dir_cmip6_inter = None
        self.dir_root_inter = None
        self.input_file = None
        self._parse_yaml(yaml_path)
        
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
        self.dir_cmip6_inter = info['dirs']['cmip6_inter']
        self.dir_root_inter = info['dirs']['root_inter']
        self.freeze_year = info['em_meta']['freeze_year']
        self.freeze_isos = info['em_meta']['freeze_isos']
        self.freeze_species = info['em_meta']['species']
       