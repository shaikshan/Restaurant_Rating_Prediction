import yaml
import numpy as np
import os,sys
from Restaurant.logger import logging
from Restaurant.exception import RestaurantException
import pandas as pd
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

def delete_columns(columns:list,df:pd.DataFrame):
    try:
        for column in df.columns:
            if column in columns:
                df.drop(columns=column,axis=1,inplace=True)
        return df
    except Exception as e:
        raise RestaurantException(e,sys) from e

def columns_removal(columns:list,df:pd.DataFrame):
        try:
            for column in df.columns:
                if column in columns:
                    df.drop(columns=column,axis=1,inplace=True)
            else:
                return df
        except Exception as e:
            raise RestaurantException(e,sys) from e 

def validate_dtype_of_column(self)->bool:
        try:
            dtype_validation = None
            logging.info(f"Validation status of both test and train:{dtype_validation}")
            schema_file_path = self.data_validation_config.schema_file_path
            schema_file_content = read_yaml_file(schema_file_path)

            train_df,test_df = self.get_train_and_test_df()



            train_df['approx_cost(for two people)'] = train_df['approx_cost(for two people)'].str.replace(",","")
            test_df['approx_cost(for two people)'] = test_df['approx_cost(for two people)'].str.replace(",","")
            
            train_df['approx_cost(for two people)']= pd.to_numeric(train_df['approx_cost(for two people)'])
            test_df['approx_cost(for two people)'] = pd.to_numeric(test_df['approx_cost(for two people)'])
            
            schema_columns_info = schema_file_content['columns']
            for key in schema_columns_info.keys():
                if train_df.dtypes[key] != schema_columns_info[key]:
                    dtype_validation = False
                    logging.info(f"Validation of train_df:{dtype_validation}")
                    return dtype_validation
                if test_df.dtypes[key] != schema_columns_info[key]:
                    dtype_validation = False
                    logging.info(f"Validation of test_df:{dtype_validation}")
                    return dtype_validation
                else:
                    dtype_validation = True
                    logging.info(f"Validation of test and train:{dtype_validation}")
            return dtype_validation
        except Exception as e:
            raise RestaurantException(e,sys) from e