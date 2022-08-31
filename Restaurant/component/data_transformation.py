from tkinter import E
from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.entity.config_entity import DataTransformationConfig
from Restaurant.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
import os,sys
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from Restaurant.constants import *
from Restaurant.util.util import *

# name: object
# online_order: object
# book_table: object
# rate: float64
# votes: int64
# location: object
# rest_type: object
# dish_liked: object                     
# cuisines: object                        
# approx_cost(for two people): float64                                           
# listed_in(type): object               
# listed_in(city): object




class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                data_ingestion_artifact:DataIngestionArtifact,
                data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_train_test_df(self):
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            train_df = pd.read_csv(train_file_path)
            logging.info(f"Loading training dataset from {train_file_path}")
            
            #train_df['Rate'] = train_df['rate']
            #logging.info(f"Creating Rate column")
            
            #train_df = train_df.drop(columns=['rate'],axis=1,inplace=True)
            #logging.info(f"Droping rate column")
            
            test_df = pd.read_csv(test_file_path)
            #logging.info(f"Loading testing dataset from {test_file_path}")
            
            #test_df['Rate'] = test_df['rate']
            #logging.info(f"Creating Rate column")
            
            #test_df = test_df.drop(columns=['rate'],axis=1,inplace=True)
            #logging.info(f"Droping rate column")

            return train_df,test_df
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def check_and_change_dtypes(self)->pd.DataFrame:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            train_df,test_df = self.get_train_test_df()
            logging.info(f"Loading train_df,and test_df")

            train_df['approx_cost(for two people)'] = train_df['approx_cost(for two people)'].str.replace(",","")
            train_df['approx_cost(for two people)'] = pd.to_numeric(train_df['approx_cost(for two people)'])
            logging.info(f"changing approx column into float")

            test_df['approx_cost(for two people)'] = test_df['approx_cost(for two people)'].str.replace(",","")
            test_df['approx_cost(for two people)'] = pd.to_numeric(test_df['approx_cost(for two people)'])
            logging.info(f"changing approx column into float")

            train_df['online_order'] = train_df['online_order'].astype('category')
            train_df['book_table']= train_df['book_table'].astype('category')
            logging.info(f"changing dtype of online_order,book_table into category")

            
            test_df['online_order'] = test_df['online_order'].astype('category')
            test_df['book_table']= test_df['book_table'].astype('category')
            logging.info(f"changing dtype of online_order,book_table into category")
            train_df['dish_liked'] = train_df['dish_liked'].apply(count)
            train_df['cuisines'] = train_df['cuisines'].apply(count)
            logging.info(f"changing dish_liked,cuisines into int64 by decoding it into numbers")

            test_df['dish_liked'] = test_df['dish_liked'].apply(count)
            test_df['cuisines'] = test_df['cuisines'].apply(count)
            logging.info(f"changing dish_liked,cuisines into int64 by decoding it into numbers")

            train_df = load_data(dataframe=train_df,schema_file_path=schema_file_path)

            test_df = load_data(dataframe=test_df,schema_file_path=schema_file_path)

            return train_df,test_df

        except Exception as e:
            raise RestaurantException(e,sys) from e

    def removing_columns(self)->pd.DataFrame:
        try:
            columns = ['name','location','rest_type','listed_in(type)','listed_in(city)']
            train_df,test_df = self.check_and_change_dtypes()
            logging.info(f"Loading train_df, test_df from check_and_change_dtypes function:")
            
            train_df = columns_removal(columns=columns,df=train_df)
            logging.info(f"Removing columns of list:{columns}")

            test_df = columns_removal(columns=columns,df=test_df)
            logging.info(f"Removing columns of list:{columns}")

            return train_df,test_df
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def detect_remove_outliers(self)->pd.DataFrame:
        try:
            pass
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_preprocessing_object(self):
        try:
            pass
        except Exception as e:
            raise RestaurantException(e,sys) from e

    