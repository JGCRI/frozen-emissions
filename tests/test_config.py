"""
Test initialization of the global constant CONFIG

Matt Nicholson
10 Feb 2020
"""
import unittest
import sys

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config
import init_config

class TestConfig(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_config_class(self):
        """Test basic CONFIG global constant initialization
        """
        config_class = config.CONFIG.__class__.__name__
        self.assertEqual(config_class, 'ConfigObj')
    
    def test_config_freeze_species(self):
        """Test expected values of CONFIG freeze_species
        """
        species_list = ['BC', 'CH4', 'CO', 'CO2', 'NH3', 'NMVOC', 'NOx', 'OC', 'SO2']
        self.assertIsInstance(config.CONFIG.freeze_species, list)
        self.assertEqual(species_list, config.CONFIG.freeze_species)
    
    def test_config_freeze_year(self):
        """Test expected values of CONFIG freeze_year
        """
        self.assertEqual(1970, config.CONFIG.freeze_year)    # Freeze year
    
    def test_config_freeze_isos(self):
        """Test expected values of CONFIG freeze_isos
        """
        self.assertEqual('all', config.CONFIG.freeze_isos)   # Freeze ISOs
    
    def test_config_ceds_meta(self):
        """Test expected values of CONFIG ceds_meta dict
        """
        self.assertEqual(1750, config.CONFIG.ceds_meta['year_first']) # CEDS first year
        self.assertEqual(2014, config.CONFIG.ceds_meta['year_last'])  # CEDS last year
        
    def test_config_path_root(self):
        """Test expected value of CONFIG root directory path
        """
        root_path = "C:\\Users\\nich980\\code\\frozen-emissions"
        self.assertEqual(config.CONFIG.dirs['root'], root_path)
    
    def test_config_path_input(self):
        """Test expected value of CONFIG input directory path
        """
        input_path = "C:\\Users\\nich980\\code\\frozen-emissions\\input"
        self.assertEqual(config.CONFIG.dirs['input'], input_path)
        
    def test_config_path_output(self):
        """Test expected value of CONFIG output directory path
        """
        input_path = "C:\\Users\\nich980\\code\\frozen-emissions\\output"
        self.assertEqual(config.CONFIG.dirs['output'], input_path)
        

# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()