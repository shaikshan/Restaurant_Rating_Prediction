from cgi import test
import zipfile
from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.entity.artifact_entity import DataIngestionArtifact
from Restaurant.entity.config_entity import DataIngestionConfig
import os,sys
from zipfile import ZipFile
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np
from scipy import stats as st
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
                        
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise RestaurantException(e,sys) from e
    @staticmethod
    def str_to_float(value:pd.DataFrame):
        try:
            if value=="NEW" or value=="-":
                value = np.nan
                return value
            else:
                value = str(value).split("/")
                value = float(value[0])
                return value
        except Exception as e:
            raise RestaurantException(e,sys) from e
    def download_restaurant_data(self,)->str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #folder location to download file
            zip_download_dir = self.data_ingestion_config.zip_download_dir

            os.makedirs(zip_download_dir,exist_ok=True)
            restaurant_file_name = "archive.zip"
            
            zip_file_path = os.path.join(zip_download_dir,restaurant_file_name)

            logging.info(f"Downloading file from {download_url} into:{[zip_file_path]}")
            urllib.request.urlretrieve(download_url,zip_file_path)
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
            with ZipFile(zip_file_path,"r") as zip:
                zip.extractall(path=raw_data_dir)
            logging.info(f"Extraction completed")
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            restaurant_file_path = os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file:[{restaurant_file_path}]")

            restaurant_data_frame = pd.read_csv(restaurant_file_path)
            logging.info(f"Converting rate column from str to float")
            restaurant_data_frame['rate'] = restaurant_data_frame['rate'].apply(str_to_float)
            logging.info(f"Converted rate column:[{restaurant_data_frame['rate'].loc[0]}]")
            
            restaurant_data_frame['rate'] = restaurant_data_frame['rate'].fillna(st.mode(restaurant_data_frame['rate'],axis=None,nan_policy='omit').mode[0])
            logging.info(f"Filling Nan values:{[restaurant_data_frame['rate'].isnull().sum()]}")

            restaurant_data_frame['extra'] = pd.cut(restaurant_data_frame["rate"],
                                                        bins=[0.0,1.0,2.0,3.0,5.0,np.inf],
                                                        labels=[1,2,3,4,5,6])

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None
            
            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2,random_state=42)

            for train_ind,test_ind in split.split(restaurant_data_frame,restaurant_data_frame['extra']):
                strat_train_set = restaurant_data_frame.loc[train_ind].drop(['extra'],axis=1)
                strat_test_set = restaurant_data_frame.loc[test_ind].drop(['extra'],axis=1)

            train_file_path = os.join.path(self.data_ingestion_config.ingested_train_dir,file_name)

            test_file_path = os.join.path(self.data_ingestion_config.ingested_test_dir,file_name)

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