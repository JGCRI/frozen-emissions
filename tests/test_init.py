"""
Test cases to test the functionality of reading YAML input files and 
initializing new ConfigObj class objects

Matt Nicholson
10 Feb 2020
"""
import unittest
import sys

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config_obj

class TestInit(unittest.TestCase):

    f_init = '../init/test-config.yml'
    
    def setup(self):
        pass
    
    def test_parse_basic(self):
        """Test basic YAML input file reading & ConfigObj instantiation
        """
        config = config_obj.ConfigObj(TestInit.f_init)
        config_class = config.__class__.__name__
        self.assertEqual(config_class, 'ConfigObj')
    
    def test_parse_winPaths(self):
        """Check that the path formats are correct for Windows. Only runs if 
        the detected OS executing the script is Windows.
        """
        if (not sys.platform.startswith('win')):
            pass
        else:
            config = config_obj.ConfigObj(TestInit.f_init)
            paths = ['cmip6', 'inter_out', 'proj_root']
            for path in paths:
                self.assertEqual(config.dirs[path].split("\\")[0], "C:")
        
    def test_init_configObj(self):
        """Check that expected ConfigObjs are present and valid
        """
        config = config_obj.ConfigObj(TestInit.f_init)
        self.assertIsInstance(config.dirs, dict)
        self.assertIsInstance(config.dirs['cmip6'], str)
        self.assertIsInstance(config.dirs['inter_out'], str)
        self.assertIsInstance(config.dirs['proj_root'], str)
        self.assertIsInstance(config.dirs['input'], str)
        self.assertIsInstance(config.dirs['output'], str)
        self.assertIsInstance(config.dirs['logs'], str)
        self.assertIsInstance(config.dirs['init'], str)
        self.assertIsInstance(config.freeze_year, int)
        self.assertIsInstance(config.freeze_isos, str)
        self.assertIsInstance(config.freeze_species, list)
        self.assertIsInstance(config.init_file, str)



# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()