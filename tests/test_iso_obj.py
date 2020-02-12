"""
Tests for the ISO class and it's methods

Matt Nicholson
12 Feb 2020
"""
import unittest
import sys
import os
import pandas as pd

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config
import isos
import test_utils

class TestInit(unittest.TestCase):
    
    def setUp(self):
        # Vars needed for initialization
        self.f_init = '../init/test-config.yml'
        self.f_ef = 'H.BC_total_EFs_extended.csv'
        self.species = 'BC'
        # Set up global CONFIG constant
        config.CONFIG = config.ConfigObj(self.f_init)
        ef_path = os.path.join(config.CONFIG.dirs['cmip6'], self.f_ef)
        self.ef_df = pd.read_csv(ef_path, sep=',', header=0)
        # Create some Iso instances
        self.usa = isos.ISO('usa', self.species, self.ef_df.loc[self.ef_df['iso'] == 'usa'])  # USA
        self.can = isos.ISO('can', self.species, self.ef_df.loc[self.ef_df['iso'] == 'can'])  # Canada
        self.mex = isos.ISO('mex', self.species, self.ef_df.loc[self.ef_df['iso'] == 'mex'])  # Mexico
    
    def test_get_sectors(self):
        """Test the get_sectors() method
        Test Case 1
        """
        self.assertEqual(sorted(self.usa.get_sectors()), test_utils.expected_sectors)
        self.assertEqual(sorted(self.can.get_sectors()), test_utils.expected_sectors)
        self.assertEqual(sorted(self.mex.get_sectors()), test_utils.expected_sectors)
    
    def test_get_fuels(self):
        """Test the get_fuels() method
        Test Case 2
        """
        self.assertEqual(sorted(self.usa.get_fuels()), test_utils.expected_fuels)
        self.assertEqual(sorted(self.can.get_fuels()), test_utils.expected_fuels)
        self.assertEqual(sorted(self.mex.get_fuels()), test_utils.expected_fuels)
        
    def test_get_species(self):
        """Test the get_species() method
        Test Case 3
        """
        self.assertEqual(self.usa.get_species(), self.species)
        self.assertEqual(self.can.get_species(), self.species)
        self.assertEqual(self.mex.get_species(), self.species)
        
    def test_get_efs(self):
        """Test the get_efs() method
        Test Case 4
        """
        expected_usa = test_utils.subset_df(self.ef_df, 'usa')
        expected_can = test_utils.subset_df(self.ef_df, 'can')
        expected_mex = test_utils.subset_df(self.ef_df, 'mex')
        
        self.assertTrue(expected_usa.equals(self.usa.get_efs()))
        self.assertTrue(expected_can.equals(self.can.get_efs()))
        self.assertTrue(expected_mex.equals(self.mex.get_efs()))
        
# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()