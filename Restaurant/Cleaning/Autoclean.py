from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
import os,sys
import pandas as pd
from Restaurant.constants import *
from Restaurant.util.util import *


class Autoclean:
    def process(self,df:pd.DataFrame,schema_path:str):
        try:
            df['approx_cost(for two people)'] = df['approx_cost(for two people)'].apply(Autoclean.handle_cost)
            logging.info(f"Changing approx_cost column into float:{df['approx_cost(for two people)'].loc[0]}")
            
            columns_ = ['online_order','book_table','listed_in(type)']
            df = Autoclean.cat(columns=columns_,df=df)
            logging.info(f"Changing columns:{columns_} into category dtype")
            
            df['cuisines'] = df['cuisines'].apply(Autoclean.count)
            logging.info(f"Changing cuisines column into int64 dtype")

            df = Autoclean.load_data(dataframe=df,schema_file_path=schema_path)
            
            columns = ['name','rest_type','location','dish_liked','listed_in(city)']
            df = Autoclean.columns_removal(columns=columns,df=df)
            logging.info(f"Removing columns from dataset columns:{columns}")
            
            df = Autoclean.cap_data(df=df)
            logging.info(f"Checking and Cleaning Outliers")

            return df
        except Exception as e:
            raise RestaurantException(e,sys) from e
    @staticmethod
    def handle_cost(value):
        try:
            if type(value) == str:
                value = str(value).replace(',',"")
                return float(value)
            else:
                return value
        except Exception as e:
            raise RestaurantException(e,sys) from e
    @staticmethod
    def cat(columns:list,df:pd.DataFrame):
        try:
            for column in df.columns:
                if column in columns:
                    df[column]=df[column].astype('category')
            return df
        except Exception as e:
            raise RestaurantException(e,sys) from e
    @staticmethod     
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
    @staticmethod     
    def columns_removal(columns:list,df:pd.DataFrame):
        try:
            for column in df.columns:
                if column in columns:
                    df.drop(columns=column,axis=1,inplace=True)
            else:
                return df
        except Exception as e:
            raise RestaurantException(e,sys) from e
    @staticmethod       
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

    @staticmethod
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