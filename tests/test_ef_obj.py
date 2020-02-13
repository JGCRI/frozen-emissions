"""
Tests for the EmissionFactorFile class and it's methods

Matt Nicholson
12 Feb 2020
"""
import unittest
import sys
import os

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config
import emission_factor_file
import test_utils

class TestInit(unittest.TestCase):
    
    def setUp(self):
        # Vars needed for initialization
        self.f_init = 'input/test-config.yml'
        self.f_ef = 'H.BC_total_EFs_extended.csv'
        self.species = 'BC'
        # Set up global CONFIG constant
        config.CONFIG = config.ConfigObj(self.f_init)
        self.ef_path = os.path.join(config.CONFIG.dirs['cmip6'], self.f_ef)
        # Create new EmissionFactorFile instance
        self.ef_obj = emission_factor_file.EmissionFactorFile(self.species, self.ef_path)
    
    def test_init(self):
        """Test basic initialization of an instance
        Test Case 1
        """
        self.assertEqual(self.ef_obj.get_shape(), (54772, 269))
        self.assertEqual(self.ef_obj.species, 'BC')
        self.assertEqual(config.CONFIG.freeze_isos, 'all')
    
    def test_get_species(self):
        """Test the get_species() function
        Test Case 2
        """
        self.assertEqual(self.ef_obj.get_species(), 'BC')
    
    def test_get_path(self):
        """Test the get_path() function
        Test Case 3
        """
        self.assertEqual(self.ef_obj.get_path(), self.ef_path)
    
    def test_get_sectors(self):
        """Test the get_sectors() function
        Test Case 4
        """
        self.assertEqual(sorted(self.ef_obj.get_sectors()), test_utils.expected_sectors)
    
    def test_get_fuels(self):
        """Test the get_fuels() function
        Test Case 5
        """
        self.assertEqual(sorted(self.ef_obj.get_fuels()), test_utils.expected_fuels)
        
    def test_isos(self):
        """Test that all the ISOs are present
        Test Case 6
        """
        self.assertEqual(sorted(self.ef_obj.get_isos()), test_utils.expected_isos)
        self.assertEqual(sorted(self.ef_obj.get_isos(ef='all')), test_utils.expected_isos)
        
# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()