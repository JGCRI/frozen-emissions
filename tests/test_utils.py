"""
Tests for utility functions, mostly from src/utils.py

Matt Nicholson
18 Feb 2020
"""
import unittest
import sys
import os

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import utils
import utils_for_tests

test_log = utils_for_tests.init_test_log('test_diagnostics')
test_log.info('Hello from test_diagnostics.py!')

class TestUtils(unittest.TestCase):
    """
    Test functions in utils.py
    """
    
    def test_get_root_dir(self):
        """
        Check that utils.get_root_dir() returns the correct directory
        """
        root_actual = os.path.join('C:\\', 'Users', 'nich980', 'code', 'frozen-emissions')
        root_test   = utils.get_root_dir()
        self.assertEqual(root_test, root_actual)
    # --------------------------------------------------------------------------


# ==============================================================================
# ==================================== Main ====================================
# ==============================================================================

if __name__ == '__main__':
    unittest.main()