"""
Tests that insure only combustion-related sectors have been "frozen" (read: modified)

Matt Nicholson
13 Feb  2020
"""
import unittest
import sys
import os

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config
import emission_factor_file
import test_utils
import driver

class TestInit(unittest.TestCase):
    
    def setUp(self):
        # Vars needed for initialization
        self.f_init = 'input/test-config.yml'
        self.species = 'BC'
        # Initialize global CONFIG object
        config.CONFIG = config.ConfigObj(self.f_init)
        self.ef_path = os.path.join(config.CONFIG.dirs['cmip6'], self.f_ef)
        # Use an un-edited CMIP6 EF file as a control
        self.f_control = r"C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output"
        # Set up an EF file object that we'll freeze
        self.f_frozen = 'H.BC_total_EFs_extended.csv'
        self.ef_obj = emission_factor_file.EmissionFactorFile(self.species, self.ef_path)
        # Freeze and calculate emissions
        driver.freeze_emissions()
        driver.calc_emissions()
        
    
        