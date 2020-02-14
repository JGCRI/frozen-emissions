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
        cls.f_control    = r'C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output\H.BC_total_EFs_extended.csv'
        test_log.debug('Test species...........{}'.format(cls.species))
        test_log.debug('Test EF file...........{}'.format(cls.f_em_factors))
        test_log.debug('Test CONFIG file.......{}'.format(cls.config_file))
        test_log.debug('Test cnotrol EF file...{}'.format(cls.f_control))
        
        # Point the CONFIG intermediate output directory to tests/input/
        config.CONFIG = config.ConfigObj(cls.config_file)
        config.CONFIG.dirs['output'] = 'input'
        
        # Freeze the emissions factors and calculate the final frozen emissions
        test_log.debug('Executing driver.freeze_emissions()')
        driver.freeze_emissions()
        test_log.debug('Executing driver.calc_emissions()')
        driver.calc_emissions()
        
        # Read the frozen emissions in to a dataframe
        test_log.debug('Reading frozen EF file into DataFrame')
        cls.f_frozen = os.path.join(config.CONFIG.dirs['output'], cls.f_em_factors)
        cls._frozen_df = pd.read_csv(cls.f_frozen, sep=',', header=0)
        
        # Read the un-edited control CMIP6 EF file
        test_log.debug('Reading control EF file into DataFrame')
        cls._control_df = pd.read_csv(cls.f_control, sep=',', header=0)
    # --------------------------------------------------------------------------
    
    def setUp(self):
        """
        Prior to each test method, create a fresh copy of the setUpClass frozen
        EF & control EF DataFrames
        """
        self.frozen_df = self._frozen_df.copy()
        self.control_df = self._control_df.copy()
    # --------------------------------------------------------------------------
    
    def test_output_shapes(self):
        """
        Test that the control DF and frozen DF have identical shapes. Should
        always pass since calc_emissions() will fail if they have mismatched
        shapes, but ya never know what be going on
        """
        test_log.debug('--- In TestFreezeAll::test_output_shapes ---')
        self.assertEqual(self.frozen_df.shape, self.control_df.shape)
    # --------------------------------------------------------------------------
    
    def test_frozen_factors_1(self):
        """
        Basic test to check that the control EF file and the frozen EF file 
        are not identical
        """
        result = True
        test_log.debug('--- In TestFreezeAll::test_frozen_factors_1 ---')
        try:
            pd.testing.assert_frame_equal(self.control_df, self.frozen_df, check_dtype=False)
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
        control_df = self.control_df[year_headers].copy()
        frozen_df  = self.frozen_df[year_headers].copy()
        try:
            pd.testing.assert_frame_equal(control_df, frozen_df, check_dtype=False)
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
        control_non_combust = test_utils.subset_noncombust_sectors(self.control_df)
        frozen_non_combust  = test_utils.subset_noncombust_sectors(self.frozen_df)
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
# ========================== TestCase TestFreezeUSA ============================
# ==============================================================================
 
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
    test_log.info('===== In TestCase TestFreezeUSA =====')
    
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
        super(TestFreezeUSA, cls).setUpClass()
        test_log.info('--- In TestFreezeUSA::setUpClass ---')
        cls.species      = 'BC'
        cls.f_em_factors = 'H.BC_total_EFs_extended.csv'
        cls.config_file  = 'input/config-test_frozen_sectors_usa.yml'
        cls.f_control    = r'C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output\H.BC_total_EFs_extended.csv'
        test_log.debug('Test species...........{}'.format(cls.species))
        test_log.debug('Test EF file...........{}'.format(cls.f_em_factors))
        test_log.debug('Test CONFIG file.......{}'.format(cls.config_file))
        test_log.debug('Test cnotrol EF file...{}'.format(cls.f_control))
        
        # Point the CONFIG intermediate output directory to tests/input/
        config.CONFIG = config.ConfigObj(cls.config_file)
        config.CONFIG.dirs['output'] = 'input'
        
        # Freeze the emissions factors and calculate the final frozen emissions
        test_log.debug('Executing driver.freeze_emissions()')
        driver.freeze_emissions()
        test_log.debug('Executing driver.calc_emissions()')
        driver.calc_emissions()
        
        # Read the frozen emissions in to a dataframe
        test_log.debug('Reading frozen EF file into DataFrame')
        cls.f_frozen = os.path.join(config.CONFIG.dirs['output'], cls.f_em_factors)
        cls._frozen_df = pd.read_csv(cls.f_frozen, sep=',', header=0)
        
        # Read the un-edited control CMIP6 EF file
        test_log.debug('Reading control EF file into DataFrame')
        cls._control_df = pd.read_csv(cls.f_control, sep=',', header=0)
    # --------------------------------------------------------------------------
    
    def setUp(self):
        """
        Prior to each test method, create a fresh copy of the setUpClass frozen
        EF & control EF DataFrames
        """
        self.frozen_df = self._frozen_df.copy()
        self.control_df = self._control_df.copy()
    # --------------------------------------------------------------------------
    
    def test_output_shapes(self):
        """
        Test that the control DF and frozen DF have identical shapes. Should
        always pass since calc_emissions() will fail if they have mismatched
        shapes, but ya never know what be going on
        """
        test_log.debug('--- In TestFreezeUSA::test_output_shapes ---')
        self.assertEqual(self.frozen_df.shape, self.control_df.shape)
    # --------------------------------------------------------------------------
    
    def test_frozen_factors_1(self):
        """
        Basic test to check that the control EF file and the frozen EF file 
        are not identical
        """
        result = True
        test_log.debug('--- In TestFreezeUSA::test_frozen_factors_1 ---')
        try:
            pd.testing.assert_frame_equal(self.control_df, self.frozen_df, check_dtype=False)
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
        test_log.debug('--- In TestFreezeUSA::test_frozen_factors_2 ---')
        year_first   = config.CONFIG.ceds_meta['year_first']
        year_freeze  = config.CONFIG.freeze_year
        year_headers = test_utils.get_year_headers(year_first, year_freeze, mode='excl')
        control_df = self.control_df[year_headers].copy()
        frozen_df  = self.frozen_df[year_headers].copy()
        try:
            pd.testing.assert_frame_equal(control_df, frozen_df, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_sectors_1(self):
        """
        Insure that non-combustion sectors for all ISOs were not changed during the 
        freezing process
        """
        result = True
        test_log.debug('--- In TestFreezeUSA::test_frozen_sectors_1 ---')
        # Get subsets of the frozen & control dataframes that only contain EFs 
        # from non-combustion sectors
        control_non_combust = test_utils.subset_noncombust_sectors(self.control_df)
        frozen_non_combust  = test_utils.subset_noncombust_sectors(self.frozen_df)
        
        try:
            pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_sectors_2(self):
        """
        Insure that non-combustion sectors for USA ISO were not changed during the 
        freezing process
        """
        result = True
        test_log.debug('--- In TestFreezeUSA::test_frozen_sectors_1 ---')
        # Get subsets of the frozen & control dataframes that only contain EFs 
        # from non-combustion sectors
        control_non_combust = test_utils.subset_noncombust_sectors(self.control_df)
        frozen_non_combust  = test_utils.subset_noncombust_sectors(self.frozen_df)
        
        # Subset USA ISO EFs
        control_non_combust = test_utils.subset_iso(control_non_combust, config.CONFIG.freeze_isos)
        frozen_non_combust  = test_utils.subset_iso(frozen_non_combust, config.CONFIG.freeze_isos)
        
        try:
            pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result)
    # --------------------------------------------------------------------------
    
    def test_frozen_isos_1(self):
        """
        Check that the EFs for the frozen USA ISO are not equal to the control USA EFs
        """
        result = True
        test_log.debug('--- In TestFreezeUSA::test_frozen_isos_1 ---')
        # Get subsets of the frozen & control dataframes that only contain EFs 
        # from non-combustion sectors
        control_non_combust = test_utils.subset_combust_sectors(self.control_df)
        frozen_non_combust  = test_utils.subset_combust_sectors(self.frozen_df)
        
        # Subset USA ISO EFs
        control_non_combust = test_utils.subset_iso(control_non_combust, config.CONFIG.freeze_isos)
        frozen_non_combust  = test_utils.subset_iso(frozen_non_combust, config.CONFIG.freeze_isos)
        
        try:
            pd.testing.assert_frame_equal(control_non_combust, frozen_non_combust, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertFalse(result) # assertFalse since we *don't* want the DFs to be equal
    # --------------------------------------------------------------------------
    
    def test_frozen_isos_2(self):
        """
        Check that the frozen EFs for ISOs != USA are identical to the control EFs
        """
        result = True
        test_log.debug('--- In TestFreezeUSA::test_frozen_isos_2 ---')
        
        # Inverse subset USA ISO EFs
        control_df = test_utils.subset_iso_inverse(self.control_df, config.CONFIG.freeze_isos)
        frozen_df  = test_utils.subset_iso_inverse(self.frozen_df, config.CONFIG.freeze_isos)
        
        try:
            pd.testing.assert_frame_equal(control_df, frozen_df, check_dtype=False)
        except AssertionError as err:
            result = False
        self.assertTrue(result) # assertTrue since we *do* want the DFs to be equal
    # --------------------------------------------------------------------------
       
    @classmethod
    def tearDownClass(cls):
        """
        Remove the files that were created by the setUpClass to run the test
        methods for this TestCase
        
        Similar to the setUpClass, this tearDownClass only executes once after
        all test methods have executed
        """
        super(TestFreezeUSA, cls).tearDownClass()
        test_log.debug('--- In TestFreezeUSA::tearDownClass ---')
        config.CONFIG = None
        try:
            os.remove('input/H.BC_total_EFs_extended.csv')
            test_log.debug('Successfully deleted input/H.BC_total_EFs_extended.csv')
            os.remove('input/BC_total_CEDS_emissions.csv')
            test_log.debug('Successfully deleted input/BC_total_CEDS_emissions.csv')
        except OSError as oserr:
            test_log.error(oserr)
            print(oserr)

# ==============================================================================
# ==================================== Main ====================================
# ==============================================================================

if __name__ == '__main__':
    unittest.main()