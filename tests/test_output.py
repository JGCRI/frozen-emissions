"""
Test output from freeze_emissions() & calc_emissions()

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

class TestFreezeAll(unittest.TestCase):
    """
    Unittest TestCase class to test output of the freeze_emissions() & calc_emissions()
    functions produced using the global configuration file config-test_frozen_sectors.yml
    
    Config
    -------
    file: config-test_frozen_sectors.yml
    freeze:
        year:    1970
        isos:    all
        species: [BC]
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up everything we need to test the output from the driver.py emission
        freezing functions freeze_emissions() & calc_emissions()
        
        Since its pretty expensive in terms of time to call the freeze_emissions()
        & calc_emissions() functions, we'll use a setUpClass to set up what we
        need for the test methods since setUpClass only executes onces at the
        beginning of execution (versus a setUp method, which executes before
        every test method call).
        """
        cls.species      = 'BC'
        cls.f_em_factors = 'H.BC_total_EFs_extended.csv'
        cls.config_file  = 'input/config-test_frozen_sectors.yml'
        cls.f_control    = r'C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output\H.BC_total_EFs_extended.csv'
        
        # Point the CONFIG intermediate output directory to tests/input/
        config.CONFIG = config.ConfigObj(config_file)
        config.CONFIG.dirs['inter_out'] = 'input'
        
        # Freeze the emissions factors and calculate the final frozen emissions
        driver.freeze_emissions()
        driver.calc_emissions()
        
        # Read the frozen emissions in to a dataframe
        cls.f_frozen = os.path.join(config.CONFIG.dirs['inter_out'], cls.f_em_factors)
        cls.frozen_df = pd.read_csv(f_frozen, sep=',', header=0)
        
        # Read the un-edited control CMIP6 EF file
        cls.control_df = pd.read_csv(cls.f_control, sep=',', header=0)
    # --------------------------------------------------------------------------
    
    def test_frozen_factors_1(self):
        """
        Basic test to check that the control EF file and the frozen EF file 
        are not identical
        """
        try:
            result = pd.testing.assert_frame_equal(cls.control_df, cls.frozen_df, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertFalse(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_factors_2(self):
        """
        Check that EFs prior to the specified freeze year have not been changed,
        no matter what ISO, sector, or fuel they belong to
        """
        year_first   = config.CONFIG.ceds_meta['year_first']
        year_freeze  = config.CONFIG.freeze_year
        year_headers = test_utils.get_year_headers(year_first, year_freeze, mode='excl')
        control_df = cls.control_df[[year_headers]].copy()
        frozen_df  = cls.frozen_df[[year_headers]].copy()
        try:
            result = pd.testing.assert_frame_equal(control_df, frozen_df, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_sectors(self):
        """
        Insure that non-combustion sectors were not changed during the 
        freezing process
        """
        # Get subsets of the frozen & control dataframes that only contain EFs 
        # from non-combustion sectors
        control_non_combust = test_utils.subset_combust_sectors(cls.control_df)
        frozen_non_combust  = test_utils.subset_combust_sectors(cls.frozen_df)
        try:
            result = pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result)
    # --------------------------------------------------------------------------  
    
    @classmethod
    def tearDownClass(cls):
        """
        Remove the files that were created by the setUpClass to run the test
        methods for this TestCase
        
        Similar to the setUpClass, this tearDownClass only executes once after
        all test methods have executed
        """
        config.CONFIG = None
        try:
            os.remove('input/H.BC_total_EFs_extended.csv')
            os.remove('input/BC_total_CEDS_emissions.csv')
        except OSError as oserr:
            print(oserr)
            
 # =============================================================================
 
 class TestFreezeUSA(unittest.TestCase):
    """
    Unittest TestCase class to test output of the freeze_emissions() & calc_emissions()
    functions produced using the global configuration file config-test_frozen_sectors_usa.yml
    
    Config
    -------
    file: config-test_frozen_sectors.yml
    freeze:
        year:    1970
        isos:    [usa]
        species: [BC]
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up everything we need to test the output from the driver.py emission
        freezing functions freeze_emissions() & calc_emissions()
        
        Since its pretty expensive in terms of time to call the freeze_emissions()
        & calc_emissions() functions, we'll use a setUpClass to set up what we
        need for the test methods since setUpClass only executes onces at the
        beginning of execution (versus a setUp method, which executes before
        every test method call).
        """
        cls.species      = 'BC'
        cls.f_em_factors = 'H.BC_total_EFs_extended.csv'
        cls.config_file  = 'input/config-test_frozen_sectors_usa.yml'
        cls.f_control    = r'C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output\H.BC_total_EFs_extended.csv'
        
        # Point the CONFIG intermediate output directory to tests/input/
        config.CONFIG = config.ConfigObj(config_file)
        config.CONFIG.dirs['inter_out'] = 'input'
        
        # Freeze the emissions factors and calculate the final frozen emissions
        driver.freeze_emissions()
        driver.calc_emissions()
        
        # Read the frozen emissions in to a dataframe
        cls.f_frozen = os.path.join(config.CONFIG.dirs['inter_out'], cls.f_em_factors)
        cls.frozen_df = pd.read_csv(f_frozen, sep=',', header=0)
        
        # Read the un-edited control CMIP6 EF file
        cls.control_df = pd.read_csv(cls.f_control, sep=',', header=0)
    # --------------------------------------------------------------------------
    
    def test_frozen_factors_1(self):
        """
        Basic test to check that the control EF file and the frozen EF file 
        are not identical
        """
        try:
            result = pd.testing.assert_frame_equal(cls.control_df, cls.frozen_df, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertFalse(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_factors_2(self):
        """
        Check that EFs prior to the specified freeze year have not been changed,
        no matter what ISO, sector, or fuel they belong to
        """
        year_first   = config.CONFIG.ceds_meta['year_first']
        year_freeze  = config.CONFIG.freeze_year
        year_headers = test_utils.get_year_headers(year_first, year_freeze, mode='excl')
        control_df = cls.control_df[[year_headers]].copy()
        frozen_df  = cls.frozen_df[[year_headers]].copy()
        try:
            result = pd.testing.assert_frame_equal(control_df, frozen_df, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_sectors_1(self):
        """
        Insure that non-combustion sectors were not changed during the 
        freezing process
        """
        # Get subsets of the frozen & control dataframes that only contain EFs 
        # from non-combustion sectors
        control_non_combust = test_utils.subset_combust_sectors(cls.control_df)
        frozen_non_combust  = test_utils.subset_combust_sectors(cls.frozen_df)
        
        try:
            result = pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_isos_1(self):
        """
        Check that the EFs for the frozen USA ISO are not equal to the control USA EFs
        """
        # Get subsets of the frozen & control dataframes that only contain EFs 
        # from non-combustion sectors
        control_non_combust = test_utils.subset_combust_sectors(cls.control_df)
        frozen_non_combust  = test_utils.subset_combust_sectors(cls.frozen_df
        
        # Subset USA ISO EFs
        control_non_combust = test_utils.subset_iso(control_non_combust, config.CONFIG.freeze_isos)
        frozen_non_combust  = test_utils.subset_iso(frozen_non_combust, config.CONFIG.freeze_isos)
        
        try:
            result = pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertFalse(result)
    # --------------------------------------------------------------------------
       
    @classmethod
    def tearDownClass(cls):
        """
        Remove the files that were created by the setUpClass to run the test
        methods for this TestCase
        
        Similar to the setUpClass, this tearDownClass only executes once after
        all test methods have executed
        """
        config.CONFIG = None
        try:
            os.remove('input/H.BC_total_EFs_extended.csv')
            os.remove('input/BC_total_CEDS_emissions.csv')
        except OSError as oserr:
            print(oserr)

# ==================================== Main ====================================

if __name__ == '__main__':
    unittest.main()