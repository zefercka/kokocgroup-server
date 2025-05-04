import logging
import os
from datetime import datetime


def run_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d - %(funcName)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"    
    )
    
    file_handler = logging.FileHandler(
        f'{os.path.dirname(os.path.realpath(__file__))}/logs/{datetime.now().strftime("%d-%m-%Y")}.log'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger
    
logger = run_logger(__name__)