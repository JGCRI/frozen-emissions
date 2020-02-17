"""
Compare output from the previous version of freeze_emissions() & calc_emissions()
with the updated version

Note: run with '-b' flag to suppress driver function outputs
    python test_frozen_sectors.py -b 

Matt Nicholson
17 Feb  2020
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

test_log = test_utils.init_test_log('test_output')
test_log.info('Hello from test_output.py!')

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
    test_log.info('===== In TestCase TestFreezeAll =====')
    
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
        super(TestFreezeAll, cls).setUpClass()
        test_log.info('--- In TestFreezeAll::setUpClass ---')
        cls.species      = 'BC'
        cls.f_em_factors = 'H.BC_total_EFs_extended.csv'
        cls.config_file  = 'input/config-test_frozen_sectors.yml'
        cls.f_previous   = r'C:\Users\nich980\data\e-freeze\frozen-emissions\2020-1-2\intermediate-output\H.BC_total_EFs_extended.csv'
        test_log.debug('Test species...........{}'.format(cls.species))
        test_log.debug('Test EF file...........{}'.format(cls.f_em_factors))
        test_log.debug('Test CONFIG file.......{}'.format(cls.config_file))
        test_log.debug('Test control EF file...{}'.format(cls.f_previous))
        
        # Point the CONFIG intermediate output directory to tests/input/
        config.CONFIG = config.ConfigObj(cls.config_file)
        config.CONFIG.dirs['output'] = 'input'
        
        # Freeze the emissions factors and calculate the final frozen emissions
        test_log.debug('Executing driver.freeze_emissions()')
        driver.freeze_emissions()
        test_log.debug('Executing driver.calc_emissions()')
        driver.calc_emissions()
        
        # Read the frozen emissions in to a dataframe
        test_log.debug('Reading current frozen EF file into DataFrame')
        cls.f_frozen = os.path.join(config.CONFIG.dirs['output'], cls.f_em_factors)
        cls._current_df = pd.read_csv(cls.f_frozen, sep=',', header=0)
        
        # Read the un-edited control CMIP6 EF file
        test_log.debug('Reading previous/control EF file into DataFrame')
        cls._previous_df = pd.read_csv(cls.f_previous, sep=',', header=0)
    # --------------------------------------------------------------------------
    
    def setUp(self):
        """
        Prior to each test method, create a fresh copy of the setUpClass frozen
        EF & control EF DataFrames
        """
        self.current_df = self._current_df.copy()
        self.previous_df = self._previous_df.copy()
    # --------------------------------------------------------------------------
    
    def test_output_shapes(self):
        """
        Test that the control DF and frozen DF have identical shapes. Should
        always pass since calc_emissions() will fail if they have mismatched
        shapes, but ya never know what be going on
        """
        test_log.debug('--- In TestFreezeAll::test_output_shapes ---')
        self.assertEqual(self.current_df.shape, self.previous_df.shape)
    # --------------------------------------------------------------------------
    
    def test_frozen_factors_1(self):
        """
        Basic test to check that the control EF file and the frozen EF file 
        are not identical
        """
        result = True
        test_log.debug('--- In TestFreezeAll::test_frozen_factors_1 ---')
        try:
            pd.testing.assert_frame_equal(self.previous_df, self.current_df, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertFalse(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_factors_2(self):
        """
        Check that EFs prior to the specified freeze year have not been changed,
        no matter what ISO, sector, or fuel they belong to
        """
        result = True
        test_log.debug('--- In TestFreezeAll::test_frozen_factors_2 ---')
        year_first   = config.CONFIG.ceds_meta['year_first']
        year_freeze  = config.CONFIG.freeze_year
        year_headers = test_utils.get_year_headers(year_first, year_freeze, mode='excl')
        previous_df = self.previous_df[year_headers].copy()
        current_df  = self.current_df[year_headers].copy()
        try:
            pd.testing.assert_frame_equal(previous_df, current_df, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_sectors_1(self):
        """
        Insure that non-combustion sectors were not changed during the 
        freezing process
        """
        result = True
        test_log.debug('--- In TestFreezeAll::test_frozen_sectors ---')
        # Get subsets of the frozen & control dataframes that only contain EFs 
        # from non-combustion sectors
        control_non_combust = test_utils.subset_noncombust_sectors(self.previous_df)
        frozen_non_combust  = test_utils.subset_noncombust_sectors(self.current_df)
        try:
            pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
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
        super(TestFreezeAll, cls).tearDownClass()
        test_log.debug('--- In TestFreezeAll::tearDownClass ---')
        config.CONFIG = None
        try:
            os.remove('input/H.BC_total_EFs_extended.csv')
            test_log.debug('Successfully deleted input/H.BC_total_EFs_extended.csv')
            os.remove('input/BC_total_CEDS_emissions.csv')
            test_log.debug('Successfully deleted input/BC_total_CEDS_emissions')
        except OSError as oserr:
            test_log.error(oserr)
            print(oserr)


# ==============================================================================
# ==================================== Main ====================================
# ==============================================================================

if __name__ == '__main__':
    unittest.main()