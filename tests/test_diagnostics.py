"""
Tests for functions in src/diag/diagnostics.py

Matt Nicholson
18 Feb 2020
"""
import unittest
import sys
import os
import numpy as np

# Insert src directory to Python path for importing
sys.path.insert(1, '../src/diag')

import diagnostics
import utils_for_tests

test_log = utils_for_tests.init_test_log('test_diagnostics')
test_log.info('Hello from test_diagnostics.py!')

class TestDiagnosticsHelpers(unittest.TestCase):
    """
    Test helper functions in diagnostics.py
    """

    def setUp(self):
        ef_dir = r'C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output'
        ef_files = ['H.BC_total_EFs_extended.csv', 'H.SO2_total_EFs_extended.csv']
        self.old_vals = np.asarray([0.87092298, 0.38216869, 0.98683747, 0.46684025,
                                    0.38882353, 0.24759944, 0.36155784, 0.74669823,
                                    0.44162432, 0.97376778])
                               
        self.new_vals = np.asarray([0.65823996, 0.77951791, 0.00117863, 0.78144378,
                                    0.84388923, 0.83482066, 0.35272254, 0.26101013,
                                    0.01613451, 0.84218052])                            
        self.control_vals = np.divide(np.subtract(self.new_vals, self.old_vals), self.old_vals)
        self.test_vals = diagnostics._calc_percent_change(self.old_vals, self.new_vals)
        self.species = ['BC', 'SO2']
        self.ef_paths = [os.path.join(ef_dir, x) for x in ef_files]
    # --------------------------------------------------------------------------
    
    def test_calc_percent_change_1(self):
        """
        Check that the arrays we're using to test the _calc_percent_change()
        function are valid
        """
        self.assertEqual(self.test_vals.size, 10)
        self.assertEqual(self.control_vals.size, 10)
    # --------------------------------------------------------------------------
        
    def test_calc_percent_change_2(self):
        """
        Test output from the _calc_percent_change helper function
        """
        self.assertTrue(np.array_equal(self.control_vals, self.test_vals))
    # --------------------------------------------------------------------------
    
    def test_parse_species_from_path_1(self):
        """
        Return 'BC' as the species from the path '.../H.BC_total_EFs_extended.csv'
        """
        test_species = diagnostics._parse_species_from_path(self.ef_paths[0])
        self.assertEqual(test_species, self.species[0])
    # --------------------------------------------------------------------------
    
    def test_parse_species_from_path_2(self):
        """
        Return 'SO2' as the species from the path '.../H.SO2_total_EFs_extended.csv'
        """
        test_species = diagnostics._parse_species_from_path(self.ef_paths[1])
        self.assertEqual(test_species, self.species[1])
    # --------------------------------------------------------------------------


# ==============================================================================
# ==================================== Main ====================================
# ==============================================================================

if __name__ == '__main__':
    unittest.main()