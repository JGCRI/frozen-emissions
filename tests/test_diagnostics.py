"""
Tests for functions in src/diag/diagnostics.py

Matt Nicholson
18 Feb 2020
"""
import unittest
import sys
import os
import pandas as pd
import numpy as np

# Insert src directory to Python path for importing
sys.path.insert(1, '../src/diag')

import test_utils
import diagnostics

test_log = test_utils.init_test_log('test_diagnostics')
test_log.info('Hello from test_diagnostics.py!')

class TestDiagnosticsHelpers(unittest.TestCase):
    """
    Test helper functions in diagnostics.py
    """

    def setUp(self):
        self.old_vals = np.asarray([0.87092298, 0.38216869, 0.98683747, 0.46684025,
                                    0.38882353, 0.24759944, 0.36155784, 0.74669823,
                                    0.44162432, 0.97376778])
                               
        self.new_vals = np.asarray([0.65823996, 0.77951791, 0.00117863, 0.78144378,
                                    0.84388923, 0.83482066, 0.35272254, 0.26101013,
                                    0.01613451, 0.84218052])   
                                    
        self.control_vals = np.divide(np.subtract(self.new_vals, self.old_vals), self.old_vals)
        self.test_vals = diagnostics._calc_percent_change(self.old_vals, self.new_vals)
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
        


# ==============================================================================
# ==================================== Main ====================================
# ==============================================================================

if __name__ == '__main__':
    unittest.main()