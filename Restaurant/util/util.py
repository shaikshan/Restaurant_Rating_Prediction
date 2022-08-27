import yaml
import numpy as np
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


 
def replace(value):
    try:
        if value=="NEW" or value =="-":
            value = np.nan
            return value
        else:
            value = str(value).split("/")
            value = float(value[0])
            return value
    except Exception as e:
        raise RestaurantException(e,sys) from e