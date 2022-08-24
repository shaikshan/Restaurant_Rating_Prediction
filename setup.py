from setuptools import setup,find_packages
from typing import List

#Declaring variables for setup function
PROJECT_NAME = 'Restaurant_rating_Prediction'
VERSION = "0.0.1"
AUTHOR = "ROSHAN"
DESCRIPTION = "This is my Restaurant_rating_prediction project"
#PACKAGES = ['housing']
REQUIREMENTS_FILE_NAME = 'requirements.txt'


def get_requirements_list()->List[str]:
    """
    Description: This function returns list of requirements
    mentioned in requirements.txt file.

    return: This function will return a list of names which contain
    in requirements.txt file
    """

    with open(REQUIREMENTS_FILE_NAME) as requirements_file:
        return requirements_file.readlines().remove("-e .")



setup(name=PROJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESCRIPTION,
packages=find_packages(),
install_requires = get_requirements_list())