"""
Logging functions for frozen-emission scripts

Usage
------
python main.py /path/to/config.yml

Matt Nicholson
7 Feb 2020
"""
import logging
import os

def nuke_logs(log_dir, target=None):
    """
    Remove any existing logs from the logs/ subdirectory
    
    Parameters
    -----------
    log_dir : str
        Path to the log directory
    target : str, optional
        Target log file to delete. If not given, all log files are deleted.
        Default is 'None'. 
    """
    if (target):
        if (not target.endswith('.log')):
            target = target + '.log'
        files = [target]
    else:
        files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
    for f in files:
        try:
            os.remove(os.path.join(log_dir, f))
        except:
            pass


def init_logger(log_dir, log_name, level='debug'):
    """
    Initialize a new logger
    
    Parameters
    -----------
    log_dir : str
        Path to the log directory
    log_name : str
        Name of the logger object
    level : str, optional
        Logging level. Default is 'debug'.
    
    Return
    -------
    logger : logging.Logger object
    """
    log_levels = {'debug': logging.DEBUG,
                  'info' : logging.INFO,
                  'warn' : logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL
                  }
    
    nuke_logs(log_dir, target=log_name)
    
    if (not os.path.isdir(log_dir)):
        os.mkdir(log_dir)
    
    if (not log_name.endswith('.log')):
        log_name = '{}.log'.format(log_name)
    log_path = os.path.join(log_dir, log_name)
    
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    
    handler = logging.FileHandler(log_path)
    handler.setFormatter(log_format)
        
    logger = logging.getLogger(log_name)
    logger.setLevel(log_levels[level])
    logger.addHandler(handler)
    logger.info("Log created!\n")
    
    return logger