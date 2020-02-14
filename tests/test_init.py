"""
Test cases to test the functionality of reading YAML input files and 
initializing new ConfigObj class objects

Matt Nicholson
10 Feb 2020
"""
import unittest
import sys

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config

class TestInit(unittest.TestCase):
    
    def setUp(self):
        """Initialize TestInit attributes for use in test cases.
        Not a test case
        """
        self.f_init = 'input/test-config.yml'
        self.config = config.ConfigObj(self.f_init)
    
    def test_parse_basic(self):
        """Test basic YAML input file reading & ConfigObj instantiation. 
        Test Case 1
        """
        config_class = self.config.__class__.__name__
        self.assertEqual(config_class, 'ConfigObj')
    
    def test_parse_winPaths(self):
        """Check that the path formats are correct for Windows. Only runs if 
        the detected OS executing the script is Windows. 
        Test Case 2
        """
        if (not sys.platform.startswith('win')):
            pass
        else:
            paths = ['cmip6', 'inter_out', 'proj_root']
            for path in paths:
                self.assertEqual(self.config.dirs[path].split("\\")[0], "C:")
        
    def test_init_configObj(self):
        """Check that expected ConfigObjs are present and of the correct types 
        Test Case 3
        """
        self.assertIsInstance(self.config.dirs, dict)
        self.assertIsInstance(self.config.dirs['cmip6'], str)
        self.assertIsInstance(self.config.dirs['inter_out'], str)
        self.assertIsInstance(self.config.dirs['proj_root'], str)
        self.assertIsInstance(self.config.dirs['ceds'], str)
        self.assertIsInstance(self.config.dirs['input'], str)
        self.assertIsInstance(self.config.dirs['output'], str)
        self.assertIsInstance(self.config.dirs['logs'], str)
        self.assertIsInstance(self.config.freeze_year, int)
        self.assertIsInstance(self.config.freeze_isos, str)
        self.assertIsInstance(self.config.freeze_species, list)
        self.assertIsInstance(self.config.init_file, str)
        self.assertIsInstance(self.config.init_file, str)
        self.assertIsInstance(self.config.init_file, str)
        self.assertIsInstance(self.config.ceds_meta['year_first'], int)
        self.assertIsInstance(self.config.ceds_meta['year_last'], int)
        
    def test_configObj_vals(self):
        """Test some of the values of the ConfigObj attributes
        Test Case 4
        """
        species_list = ['BC', 'CH4', 'CO', 'CO2', 'NH3', 'NMVOC', 'NOx', 'OC', 'SO2']
        self.assertIsInstance(self.config.freeze_species, list)
        self.assertEqual(species_list, self.config.freeze_species)
        self.assertEqual(1970, self.config.freeze_year)    # Freeze year
        self.assertEqual('all', self.config.freeze_isos)   # Freeze ISOs
        self.assertEqual(1750, self.config.ceds_meta['year_first']) # CEDS first year
        self.assertEqual(2014, self.config.ceds_meta['year_last'])  # CEDS last year
        
        



# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()