"""
Utility functions

Matt Nicholson
18 Feb 2020
"""
import os

def get_root_dir():
    """
    Get the project's root directory
    
    Parameters
    -----------
    None
    
    Return
    -------
    str : Absolute path of the project's root directory
    """
    root, _ = os.path.split(os.path.dirname(os.path.abspath(__file__)))
    return root

