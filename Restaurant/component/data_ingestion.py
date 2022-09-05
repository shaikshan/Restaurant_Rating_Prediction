from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.entity.config_entity import DataIngestionConfig
import os,sys
from zipfile import ZipFile
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from scipy import stats as st
from Restaurant.util.util import *
from kaggle.api.kaggle_api_extended import KaggleApi
from Restaurant.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
                        
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise RestaurantException(e,sys) from e
    def download_restaurant_data(self)->str:
        try:
            #extraction remote url to download dataset
            dataset_info = self.data_ingestion_config.dataset_info

            #folder location to download file
            zip_download_dir = self.data_ingestion_config.zip_download_dir

            os.makedirs(zip_download_dir,exist_ok=True)

            zip_file = os.path.basename(dataset_info)+".zip"

            zip_file_path = os.path.join(zip_download_dir,zip_file)

            logging.info(f"Downloading file from {dataset_info} into:{[zip_file_path]}")
            api = KaggleApi()
            api.authenticate()
            api.dataset_download_files(dataset_info,path=zip_download_dir)
            logging.info(f"File :{[zip_file_path]} has been downloaded successfully.")
            return zip_file_path
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def extract_zip_file(self,zip_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting:{zip_file_path} into dir:{raw_data_dir}")
            
            with ZipFile(zip_file_path,'r') as zip:
                zip.extractall(path=raw_data_dir)
            logging.info(f"Extraction completed")
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_restaurant_df(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            file_name = os.listdir(raw_data_dir)[0]

            restaurant_file_path = os.path.join(raw_data_dir,file_name)
            logging.info(f"Reading csv file:[{restaurant_file_path}]")

            restaurant_data_frame = pd.read_csv(restaurant_file_path)
            logging.info(f"Converting rate column from str to float")

            restaurant_data_frame['rate'] = restaurant_data_frame['rate'].apply(replace)
            logging.info(f"Converted rate column:[{restaurant_data_frame['rate'].loc[0]}]")

            restaurant_data_frame["rate"] = restaurant_data_frame['rate'].fillna(np.mean(restaurant_data_frame['rate']))
            logging.info(f"Filling Nan values:[{restaurant_data_frame['rate'].isnull().sum()}]")

            restaurant_data_frame['Rate'] = restaurant_data_frame['rate']
            logging.info(f"Creating Rate column")

            restaurant_data_frame.drop(columns=['rate'],axis=1,inplace=True)
            
            return restaurant_data_frame     
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            #restaurant_file_path = os.path.join(raw_data_dir,file_name)

            #logging.info(f"Reading csv file:[{restaurant_file_path}]")

            #restaurant_data_frame = pd.read_csv(restaurant_file_path)
            #logging.info(f"Converting rate column from str to float")
            #restaurant_data_frame['rate'] = restaurant_data_frame['rate'].apply(replace)
            #logging.info(f"Converted rate column:[{restaurant_data_frame['rate'].loc[0]}]")
            
            #restaurant_data_frame['rate'] = restaurant_data_frame['rate'].fillna(st.mode(restaurant_data_frame['rate'],axis=None,nan_policy='omit').mode[0])
            #logging.info(f"Filling Nan values:{[restaurant_data_frame['rate'].isnull().sum()]}")

            #restaurant_data_frame['Rate'] = restaurant_data_frame['rate']
            #logging.info(f"Creating Rate column")
            
            #restaurant_data_frame = restaurant_data_frame.drop('rate',axis=1,inplace=True)
            #logging.info(f"Droping rate column")

            restaurant_data_frame = self.get_restaurant_df()
            
            restaurant_data_frame['extra'] = pd.cut(restaurant_data_frame["Rate"],
                                                        bins=[0.0,1.5,3.0,4.5,np.inf],
                                                        labels=[1,2,3,4])
                                                
            logging.info(f"Shape of restaurant_dataframe:{restaurant_data_frame.shape}")
            restaurant_data_frame = restaurant_data_frame.drop_duplicates()
            logging.info(f"Shape of restaurant_dataframe:{restaurant_data_frame.shape}")

            logging.info(f"Splitting data into train and test")

            strat_train_set = None
            strat_test_set = None
            
            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2,random_state=42)

            for train_ind,test_ind in split.split(restaurant_data_frame,restaurant_data_frame['extra']):
                strat_train_set = restaurant_data_frame.loc[train_ind].drop(['extra'],axis=1)
                strat_test_set = restaurant_data_frame.loc[test_ind].drop(['extra'],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            columns=['url','address','phone','reviews_list','menu_item']
            strat_train_set = columns_removal(columns=columns,df=strat_train_set)
            logging.info(f"Removing columns:{columns}")
            strat_test_set = columns_removal(columns=columns,df=strat_test_set)
            logging.info(f"Removing columns :{columns}")
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training dataset to file:[{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting testing dataset to file:[{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                    test_file_path=test_file_path,is_ingested=True,
                                                    message=f"Data ingestion completed successfully")

            logging.info(f"DataIngestionArtifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            zip_file_path = self.download_restaurant_data()
            self.extract_zip_file(zip_file_path=zip_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")