"""
FILE: logger.py
AUTHOR: Tran Danh Lam 
CREATED: 2024-10-25
MODIFIED: 2024-11-25
DESCRIPTION: This module contains logger module.
"""

import os
import logging
from datetime import datetime
from functools import wraps
from configs import log as log_config

# ANSI escape codes for colors
RESET = "\033[0m"
YELLOW = "\033[33m"
RED = "\033[31m"

def format_log(func):
    """
    A decorator that formats log messages with a timestamp, log level, and optional color coding.
    Args:
        func (function): The logging function to be decorated.
    Returns:
        function: The wrapped function with formatted log messages.
    The decorator adds the following to the log message:
    - Current timestamp in the format "YYYY-MM-DD HH:MM:SS".
    - Log level in uppercase (derived from the function name).
    - Color coding based on the log level (yellow for WARNING, red for ERROR, no color otherwise).
    Example:
        @format_log
        def info(message):
            print(message)
        info("This is an info message.")
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_level = func.__name__.upper()
        
        # Determine color based on log level
        if log_level == 'WARNING':
            color = YELLOW
        elif log_level == 'ERROR':
            color = RED
        else:
            color = ""
        
        args = (f"{current_time}: {color}{args[0]:^30} : {args[1]}{RESET}",) + args[2:]
        return func(*args, **kwargs)
    return wrapper

logging.info = format_log(logging.info)
logging.warning = format_log(logging.warning)
logging.error = format_log(logging.error)
logging.debug = format_log(logging.debug)

 
class Logger:
   
    m_class_name = "Logger"
    m_log_folder = log_config.LOG_FOLDER_NAME
    m_log_level = log_config.LOG_LEVEL
   
    def __init__(self):
        today = datetime.today().strftime('%Y_%m_%d')
        FORMAT = '%(message)s'
        # Check and create log folder
        if not os.path.isdir(self.m_log_folder):
            os.makedirs(self.m_log_folder)
        # Set up logging
        # logging.basicConfig(
        #     level=self.m_log_level,
        #     format=FORMAT,
        #     force=True,
        #     handlers=[
        #         logging.FileHandler(f"{self.m_log_folder}/{today}.log"),
        #         logging.StreamHandler()
        #     ]
        # )
        logging.basicConfig(filename=f'{self.m_log_folder}/{today}.log', encoding='utf-8', level=self.m_log_level, force=True, format=FORMAT)
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.info("Logger", 'Init')
 
    def info(self, data):
        logging.info("Logger", data)
       
    def warning(self, data):
        logging.warning("Logger", data)
       
    def error(self, data):
        logging.error("Logger", data)