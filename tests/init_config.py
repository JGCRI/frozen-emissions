"""
Initialize a global CONFIG constant for use in test_config.py

Matt Nicholson
10 Feb 2020
"""
import sys

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config_obj
from config_obj import CONFIG

f_init = '../init/test-config.yml'

global CONFIG 
CONFIG = config_obj.ConfigObj(f_init)

def update_config():
    global CONFIG
    CONFIG.freeze_isos = ['USA']
    CONFIG.freeze_year = 2020
    CONFIG.ceds_meta['year_first'] = -1
    CONFIG.ceds_meta['year_last'] = 42069
