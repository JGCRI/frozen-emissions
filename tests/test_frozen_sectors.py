"""
Tests that insure only combustion-related sectors have been "frozen" (read: modified)

Note: run with '-b' flag to suppress driver function outputs
    python test_frozen_sectors.py -b 

Matt Nicholson
13 Feb  2020
"""
import unittest
import sys
import os
import pandas as pd

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config
import emission_factor_file
import test_utils
import driver

class TestFrozenSectors(unittest.TestCase):
    
    def setUp(self):
        self.species = 'BC'
        self.f_ef = 'H.BC_total_EFs_extended.csv'
        self.f_control = r"C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output\H.BC_total_EFs_extended.csv"
    
    def tearDown(self):
        config.CONFIG = None
        try:
            os.remove('input/H.BC_total_EFs_extended.csv')
            os.remove('input/BC_total_CEDS_emissions.csv')
        except OSError as oserr:
            print(oserr)
            
    def test_frozen_sectors_1(self):
        """Check that only combustion-related sectors were modified using 
        input/config-test_frozen_sectors.yml as the config file
        """
        f_init = 'input/config-test_frozen_sectors.yml'
        result = self._helper_frozen_sectors(f_init)
        self.assertTrue(result)
        
    def test_frozen_sectors_2(self):
        """Check that only combustion-related sectors were modified using 
        input/config-test_frozen_sectors_usa.yml as the config file
        """
        f_init = 'input/config-test_frozen_sectors_usa.yml'
        result = self._helper_frozen_sectors(f_init)
        self.assertTrue(result)
        
    def test_frozen_iso(self)
        """Check that only the USA ISO is frozen when specified in the .yml
        config file
        """
        f_init = 'input/config-test_frozen_sectors_usa.yml'
        result = self._helper_frozen_sectors(f_init)
        self.assertTrue(result)
            
    def _helper_frozen_sectors(self, config_file):
        """Helper function to do the heavy lifting and fun the emission freezing
        and creating functions. 
        """
        result = True
        # Initialize global CONFIG object
        config.CONFIG = config.ConfigObj(config_file)
        config.CONFIG.dirs['inter_out'] = 'input'
        f_frozen = os.path.join(config.CONFIG.dirs['inter_out'], self.f_ef)
        
        # Freeze and calculate emissions
        driver.freeze_emissions()
        driver.calc_emissions()
        
        # Read the frozen emissions in to a dataframe
        frozen_df = pd.read_csv(f_frozen, sep=',', header=0)
        
        # Read the un-edited control CMIP6 EF file
        control_df = pd.read_csv(self.f_control, sep=',', header=0)
        
        # Get a subset of the control & frozen DF containing only non-combustion sectors
        control_non_combust = control_df.loc[control_df['sector'].isin(test_utils.non_combustion_sectors)].copy()
        frozen_non_combust = frozen_df.loc[frozen_df['sector'].isin(test_utils.non_combustion_sectors)].copy()
        # result = control_non_combust.equals(frozen_non_combust)
        try:
            pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
        except AssertionError as err:
            result = False
        return result
    
    def _helper_frozen_iso(self, config_file):
        """Helper for test_frozen_iso
        """
        result = True
        # Initialize global CONFIG object
        config.CONFIG = config.ConfigObj(config_file)
        config.CONFIG.dirs['inter_out'] = 'input'
        f_frozen = os.path.join(config.CONFIG.dirs['inter_out'], self.f_ef)
        
        # Freeze and calculate emissions
        driver.freeze_emissions()
        driver.calc_emissions()
        
        # Read the frozen emissions in to a dataframe
        frozen_df = pd.read_csv(f_frozen, sep=',', header=0)
        
        # Read the un-edited control CMIP6 EF file
        control_df = pd.read_csv(self.f_control, sep=',', header=0)
        
        # Get a subset of the control & frozen DF containing only non-combustion sectors
        control_non_combust = control_df.loc[control_df['sector'].isin(test_utils.non_combustion_sectors)].copy()
        frozen_non_combust = frozen_df.loc[frozen_df['sector'].isin(test_utils.non_combustion_sectors)].copy()
        # result = control_non_combust.equals(frozen_non_combust)
        try:
            pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
        except AssertionError as err:
            result = False
        return result
            
# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()