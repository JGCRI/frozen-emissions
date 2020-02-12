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

class TestInit(unittest.TestCase):
    
    def setUp(self):
        # Vars needed for initialization
        self.f_init = '../init/test-config.yml'
        self.f_ef = 'H.BC_total_EFs_extended.csv'
        self.species = 'BC'
        # Set up global CONFIG constant
        config.CONFIG = config.ConfigObj(self.f_init)
        self.ef_path = os.path.join(config.CONFIG.dirs['cmip6'], self.f_ef)
        # Create new EmissionFactorFile instance
        self.ef_obj = emission_factor_file.EmissionFactorFile(self.species, ef_path)
    
    def test_init(self):
        """Test basic initialization of an instance
        Test Case 1
        """
        self.assertEqual(self.ef_obj.shape, (54772, 269))
        self.assertEqual(self.ef_obj.species, 'BC')
    
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
    
    def test_get_min_year(self):
        """Test the get_min_year() function
        Test Case 4
        """
        self.assertEqual(self.ef_obj.get_min_year(), 'X1750')
    
    def test_get_max_year(self):
        """Test the get_max_year() function
        Test Case 5
        """
        self.assertEqual(self.ef_obj.get_max_year(), 'X2014')
    
    def test_get_sectors(self):
        """Test the get_sectors() function
        Test Case 6
        """
    
        
        
    
        


# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()