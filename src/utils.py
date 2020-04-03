"""
Utility functions

Matt Nicholson
18 Feb 2020
"""
from pathlib import Path

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
    root = str(Path(os.path.abspath(__file__)).parents[1])
    return root
