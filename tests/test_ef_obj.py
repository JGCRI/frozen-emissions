"""
Tests for the EmissionFactorFile class and it's methods

Matt Nicholson
12 Feb 2020
"""
import unittest
import sys
import os

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config
import emission_factor_file

class TestInit(unittest.TestCase):
    
    def setUp(self):
        # Vars needed for initialization
        self.f_init = '../init/test-config.yml'
        self.f_ef = 'H.BC_total_EFs_extended.csv'
        self.species = 'BC'
        # Set up global CONFIG constant
        config.CONFIG = config.ConfigObj(self.f_init)
        self.ef_path = os.path.join(config.CONFIG.dirs['cmip6'], self.f_ef)
        # Create new EmissionFactorFile instance
        self.ef_obj = emission_factor_file.EmissionFactorFile(self.species, self.ef_path)
    
    def test_init(self):
        """Test basic initialization of an instance
        Test Case 1
        """
        self.assertEqual(self.ef_obj.shape, (54772, 269))
        self.assertEqual(self.ef_obj.species, 'BC')
        self.assertEqual(config.CONFIG.freeze_isos, 'all')
    
    def test_get_species(self):
        """Test the get_species() function
        Test Case 2
        """
        self.assertEqual(self.ef_obj.get_species(), 'BC')
    
    def test_get_path(self):
        """Test the get_path() function
        Test Case 3
        """
        self.assertEqual(self.ef_obj.get_path(), self.ef_path)
    
    def test_get_sectors(self):
        """Test the get_sectors() function
        Test Case 5
        """
        expected_sectors = ['1A1a_Electricity-public', '1A1a_Electricity-autoproducer',
            '1A1a_Heat-production', '1A2a_Ind-Comb-Iron-steel', '1A2b_Ind-Comb-Non-ferrous-metals',
            '1A2c_Ind-Comb-Chemicals', '1A2d_Ind-Comb-Pulp-paper', '1A2e_Ind-Comb-Food-tobacco',
            '1A2f_Ind-Comb-Non-metalic-minerals', '1A2g_Ind-Comb-Construction',
            '1A2g_Ind-Comb-transpequip', '1A2g_Ind-Comb-machinery', '1A2g_Ind-Comb-mining-quarying',
            '1A2g_Ind-Comb-wood-products', '1A2g_Ind-Comb-textile-leather', '1A2g_Ind-Comb-other',
            '1A3ai_International-aviation', '1A3aii_Domestic-aviation', '1A3b_Road',
            '1A3c_Rail', '1A3di_International-shipping', '1A3dii_Domestic-navigation',
            '1A3eii_Other-transp', '1A4a_Commercial-institutional', '1A4b_Residential',
            '1A4c_Agriculture-forestry-fishing', '1A5_Other-unspecified']
            
        self.assertEqual(sorted(self.ef_obj.get_sectors()), sorted(expected_sectors))
    
        
        
    
        


# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()