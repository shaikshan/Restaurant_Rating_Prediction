import yaml

import os,sys
from Restaurant.logger import logging
from Restaurant.exception import RestaurantException

def read_yaml_file(file_path:str):
    """
    Reads a yaml file and returns the content as a dictionary.
    file_path:str
    """
    try:
        with open(file_path,"rb") as yaml_file:
           return yaml.safe_load(yaml_file)
    except Exception as e:
        raise RestaurantException(e,sys) from e