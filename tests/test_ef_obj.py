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
        Test Case 4
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
    
    def test_get_fuels(self):
        """Test the get_fuels() function
        Test Case 5
        """
        expected_fuels = ['process', 'biomass', 'brown_coal', 'coal_coke', 'diesel_oil',
                          'hard_coal', 'heavy_oil', 'light_oil', 'natural_gas']
        self.assertEqual(sorted(self.ef_obj.get_fuels()), sorted(expected_fuels))
        
    def test_isos(self):
        """Test that all the ISOs are present
        Test Case 6
        """
        expected_isos = ['abw', 'afg', 'ago', 'alb', 'are', 'arg', 'arm', 'asm',
            'atg', 'aus', 'aut', 'aze', 'bdi', 'bel', 'ben', 'bfa', 'bgd', 'bgr',
            'bhr', 'bhs', 'bih', 'blr', 'blz', 'bmu', 'bol', 'bra', 'brb', 'brn',
            'btn', 'bwa', 'caf', 'can', 'che', 'chl', 'chn', 'civ', 'cmr', 'cod',
            'cog', 'cok', 'col', 'com', 'cpv', 'cri', 'cub', 'cuw', 'cym', 'cyp',
            'cze', 'deu', 'dji', 'dma', 'dnk', 'dom', 'dza', 'ecu', 'egy', 'eri',
            'esh', 'esp', 'est', 'eth', 'fin', 'fji', 'flk', 'fra', 'fro', 'fsm',
            'gab', 'gbr', 'geo', 'gha', 'gib', 'gin', 'global', 'glp', 'gmb', 'gnb',
            'gnq', 'grc', 'grd', 'grl', 'gtm', 'guf', 'gum', 'guy', 'hkg', 'hnd',
            'hrv', 'hti', 'hun', 'idn', 'ind', 'irl', 'irn', 'irq', 'isl', 'isr',
            'ita', 'jam', 'jor', 'jpn', 'kaz', 'ken', 'kgz', 'khm', 'kir', 'kna',
            'kor', 'kwt', 'lao', 'lbn', 'lbr', 'lby', 'lca', 'lie', 'lka', 'lso',
            'ltu', 'lux', 'lva', 'mac', 'mar', 'mda', 'mdg', 'mdv', 'mex', 'mhl',
            'mkd', 'mli', 'mlt', 'mmr', 'mne', 'mng', 'moz', 'mrt', 'msr', 'mtq',
            'mus', 'mwi', 'mys', 'nam', 'ncl', 'ner', 'nga', 'nic', 'niu', 'nld',
            'nor', 'npl', 'nzl', 'omn', 'pak', 'pan', 'per', 'phl', 'plw', 'png',
            'pol', 'pri', 'prk', 'prt', 'pry', 'pse', 'pyf', 'qat', 'reu', 'rou',
            'rus', 'rwa', 'sau', 'sdn', 'sen', 'sgp', 'slb', 'sle', 'slv', 'som',
            'spm', 'srb', 'srb (kosovo)', 'ssd', 'stp', 'sur', 'svk', 'svn', 'swe',
            'swz', 'sxm', 'syc', 'syr', 'tca', 'tcd', 'tgo', 'tha', 'tjk', 'tkl',
            'tkm', 'tls', 'ton', 'tto', 'tun', 'tur', 'twn', 'tza', 'uga', 'ukr',
            'ury', 'usa', 'uzb', 'vct', 'ven', 'vgb', 'vir', 'vnm', 'vut', 'wlf',
            'wsm', 'yem', 'zaf', 'zmb', 'zwe']
        self.assertEqual(sorted(self.ef_obj.isos.keys()), sorted(expected_isos))
        
# ------------------------------------ Main ------------------------------------

if __name__ == '__main__':
    unittest.main()