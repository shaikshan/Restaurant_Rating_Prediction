import yaml
import numpy as np
import os,sys
from Restaurant.logger import logging
from Restaurant.exception import RestaurantException
import pandas as pd
import dill
from Restaurant.constants import *

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

def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise RestaurantException(e,sys)

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise RestaurantException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise RestaurantException(e, sys) from e


def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise RestaurantException(e,sys) from e

def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
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


def count(value):
    try:
        if type(value) == float:
            value = 0
            return value
        else:
            value = len(str(value).split(","))
            return value
    except Exception as e:
        raise RestaurantException(e,sys) from e

def load_data(dataframe:pd.DataFrame, schema_file_path: str):
    try:
        datatset_schema = read_yaml_file(schema_file_path)

        schema = datatset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        error_messgae = ""
        
        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_messgae = f"{error_messgae} \nColumn: [{column}] is not in the schema."
        if len(error_messgae) > 0:
            raise Exception(error_messgae)
        return dataframe

    except Exception as e:
        raise RestaurantException(e,sys) from e


def fill_na(value,median_):
    try:
        if type(value) == float:
            value = str(value)
        if value == "nan":
            return float(median_)
        else:
            return float(value)
    except Exception as e:
        raise RestaurantException(e,sys) from e

def cap_data(df):
    try:
        for col in df.columns:
            print("capping the ",col)
            if (((df[col].dtype)=='float64') | ((df[col].dtype)=='int64')):
                percentiles = df[col].quantile([0.01,0.99]).values
                df[col][df[col] <= percentiles[0]] = percentiles[0]
                df[col][df[col] >= percentiles[1]] = percentiles[1]
            else:
                df[col]=df[col]
        return df
    except Exception as e:
        raise RestaurantException(e,sys) from e

def handle_cost(value):
    try:
        if type(value) == str:
            value = str(value).replace(',',"")
            return float(value)
    except Exception as e:
        raise RestaurantException(e,sys) from e


def cat(columns:list,df:pd.DataFrame):
    try:
        for column in df.columns:
            if column in columns:
                df[column]=df[column].astype('category')
        return df
    except Exception as e:
        raise RestaurantException(e,sys) from e