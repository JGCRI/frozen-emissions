"""
Functions to produce summary output & plots for final frozen emissions

Matt Nicholson
23 Mar 2020
"""
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

import ceds_io
import utils


CEDS_VERSION = 'v_2020_1_13'
CMIP_VERSION = 'v2016_07_26'


def plot_isos(isos='default', emissions='all'):
    """
    Create a plot with both the CMIP6 emissions and frozen emissions for each 
    emission species for a selection of ISOs
    
    Parameters
    -----------
    isos : str or list of str, optional
        ISOs to plot. Default is 'default', which results in 
        USA, Canada, China, & Russia being plotted.
    emissions : str or list of str, optional
        Emission species to plot. Default is 'all'
    """
    logger = logging.getLogger('main')
    logger.debug('In summary.py::plot_isos')
    # Directory holding the final frozen emissions files to read & plot
    in_dir  = os.path.join(utils.get_root_dir(), 'output', 'final-emissions')
    # Directory that the frozen emissions plots will be written to
    out_dir = os.path.join(utils.get_root_dir(), 'output', 'diagnostic')
    
    if emissions == 'all':
        emissions = ['BC', 'CH4', 'CO', 'CO2', 'NH3', 'NMVOC', 'NOx', 'OC', 'SO2']
    elif not isinstance(emissions, list) and emissions != 'all':
        emissions = [emissions]
        
    if isos == 'default':
        isos = ['usa', 'can', 'chn', 'rus']
    elif not isinstance(isos, list) and emissions != 'default':
        isos = [isos]
    
    logger.debug('emissions = '.format(emissions))
    logger.debug('isos = '.format(isos))
    
    # Create 3x3 facet plot
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3)
    
    idx, em in enumerate(emissions):
        # TODO: Make function for writing to logger & printing to console
        msg = 'Processing diagnostics for {}'.format(em)
        print(msg)
        logger.debug(msg)
        
        frzn_fname = 'CEDS_{}_emissions_by_country_sector_{}.csv'.format(em, CEDS_VERSION)
        frzn_fname = os.path.join(utils.get_root_dir(), 'output', 'final-emissions', frzn_fname)
        
        cmip_fname = '{}_CEDS_emissions_by_sector_country_{}.csv'.format(em, CMIP_VERSION)
        cmip_fname = os.path.join(utils.get_root_dir(), 'input', 'cmip', 'final-emissions', cmip_fname)
        
        msg = 'Reading {}...'.format(frzn_fname)
        print(msg)
        logger.debug(msg)
        frzn_df = pd.read_csv(frzn_fname, sep=',', header=0)
        
        msg = 'Reading {}...'.format(cmip_fname)
        print(msg)
        logger.debug(msg)
        cmip_df = pd.read_csv(cmip_fname, sep=',', header=0)
        
        # To be continued...
        
        
        
        
    
    