"""
Tests for the functions in ceds_io.py

Matt Nicholson
13 Feb 2020
"""
import unittest
import sys
import os

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config
import ceds_io

class TestCedsIO(unittest.TestCase):
    
    def setUp(self):
        # Vars needed for initialization
        self.f_init = 'input/config-test_frozen_sectors.yml'
        self.f_ef = 'H.BC_total_EFs_extended.csv'
        self.species = 'BC'
        # Set up global CONFIG constant
        config.CONFIG = config.ConfigObj(self.f_init)
        # self.ef_path = os.path.join(config.CONFIG.dirs['cmip6'], self.f_ef)
        ## Create new EmissionFactorFile instance
        # self.ef_obj = emission_factor_file.EmissionFactorFile(self.species, self.ef_path)
        
    def test_fetch_ef_files(self):
        """Test that fetch_ef_files() returns only EF files for species defined
        in config.CONFIG.freeze_species
        """
        expected = [self.f_ef]
        self.assertEqual(ceds_io.fetch_ef_files(config.CONFIG.dirs['cmip6']), expected)
    
    def test_fetch_ef_files_2(self):
        """Test that fetch_ef_files() returns only EF files for species defined
        in config.CONFIG.freeze_species
        """
        config.CONFIG.freeze_species = ['BC', 'SO2']
        expected = [self.f_ef, 'H.SO2_total_EFs_extended.csv' ]
        self.assertEqual(ceds_io.fetch_ef_files(config.CONFIG.dirs['cmip6']), expected)
        
# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()