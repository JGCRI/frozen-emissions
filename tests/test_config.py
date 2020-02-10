"""
Test initialization of the global constant CONFIG

Matt Nicholson
10 Feb 2020
"""
import unittest
import sys

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config_obj
from init_config import CONFIG, update_config

class TestInit(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_config_class(self):
        """Test basic CONFIG global constant initialization
        Test Case 1
        """
        config_class = CONFIG.__class__.__name__
        self.assertEqual(config_class, 'ConfigObj')
    
    def test_config_vals(self):
        """Test expected values of CONFIG attributes
        Test Case 2
        """
        species_list = ['BC', 'CH4', 'CO', 'CO2', 'NH3', 'NMVOC', 'NOx', 'OC', 'SO2']
        self.assertIsInstance(CONFIG.freeze_species, list)
        self.assertEqual(species_list, CONFIG.freeze_species)
        self.assertEqual(1970, CONFIG.freeze_year)    # Freeze year
        self.assertEqual('all', CONFIG.freeze_isos)   # Freeze ISOs
        self.assertEqual(1750, CONFIG.ceds_meta['year_first']) # CEDS first year
        self.assertEqual(2015, CONFIG.ceds_meta['year_last'])  # CEDS last year
    
    def test_update_config(self):
        """Test if updates to CONFIG in another file will be reflected here
        Test Case 3
        """
        update_config()
        
        config_class = CONFIG.__class__.__name__
        self.assertEqual(config_class, 'ConfigObj')
        self.assertEqual(2020, CONFIG.freeze_year)              # Freeze year
        self.assertEqual(['USA'], CONFIG.freeze_isos)           # Freeze ISOs
        self.assertEqual(-1, CONFIG.ceds_meta['year_first'])    # CEDS first year
        self.assertEqual(42069, CONFIG.ceds_meta['year_last'])  # CEDS last year
        


# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()