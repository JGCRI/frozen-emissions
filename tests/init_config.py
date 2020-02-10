"""
Initialize a global CONFIG constant for use in test_config.py

Matt Nicholson
10 Feb 2020
"""
import sys

# Insert src directory to Python path for importing
sys.path.insert(1, '../src')

import config

f_init = '../init/test-config.yml'

config.CONFIG = config.ConfigObj(f_init)

def update_config():
    config.CONFIG.freeze_isos = ['USA']
    config.CONFIG.freeze_year = 2020
    config.CONFIG.ceds_meta['year_first'] = -1
    config.CONFIG.ceds_meta['year_last'] = 42069
