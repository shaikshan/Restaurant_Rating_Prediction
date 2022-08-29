from cgi import test
from email import message
from operator import index
from Restaurant.logger import logging
from Restaurant.exception import RestaurantException
import os,sys
import pandas as pd
from Restaurant.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from Restaurant.entity.config_entity import DataValidationConfig
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json
from Restaurant.util.util import *

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                    data_validation_config:DataValidationConfig):
        try:
            logging.info(f"{'>>'*30}Data Valdaition log started.{'<<'*30} \n\n")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist
            logging.info(f"is train and test file exists?->{is_available}")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file:{training_file} or Testing file:{testing_file}"\
                    "is not present"
                raise Exception(message)
            return is_available
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            validation_status = None
            schema_file_path = self.data_validation_config.schema_file_path

            schema_file_info = read_yaml_file(schema_file_path)

            schema_columns_info = schema_file_info['columns']

            train_df,test_df = self.get_train_and_test_df()

            train_columns_len = len(schema_columns_info) == len(train_df.columns)

            test_columns_len = len(schema_columns_info) == len(test_df.columns)

            equal_len = train_columns_len and test_columns_len

            if not equal_len:
                validation_status = equal_len
                logging.info(f"Validating Schema of dataset:{validation_status}")
                return validation_status
            else:
                validation_status = equal_len
                logging.info(f"Validating Schema of dataset:{validation_status}")
                return validation_status
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def column_name_check(self)->bool:
        try:
            schema_file_path = self.data_validation_config.schema_file_path
            schema_file_content = read_yaml_file(schema_file_path)
            schema_columns_info = schema_file_content['columns']
            train_df,test_df = self.get_train_and_test_df()

            validation = True
            if len(schema_columns_info.keys())==len(train_df.columns):
                i =0
                for key in schema_columns_info.keys():
                    if train_df.dtypes.index[i] != key:
                        message = "Columns name is not found"
                        logging.info(f"Validation of column names:{message}")
                    i+= 1
                logging.info(f"Validation status of train_df :{validation}")
            if len(schema_columns_info.keys()) == len(test_df.columns):
                j=0
                for key in schema_columns_info.keys():
                    if test_df.dtypes.index[j] != key:
                        message = "Columns name is not found"
                        logging.info(f"Validation of column names:{message}")
                    j+=1
                logging.info(f"Validation status of test_df:{validation}")
                return validation
            else:
                logging.info(f"Length of train_df and test_df are not equal to schema_columns_keys len()")
                logging.info(f"Validation Done:{validation}")
                return validation
        except Exception as e:
            raise RestaurantException(e,sys) from e    
        
    def get_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,'w') as report_file:
                json.dump(report,report_file,indent=6)
            return report
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def save_data_drift_report(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise RestaurantException(e,sys) from e
    
    def is_data_drift_found(self)->bool:
        try:
            report = self.get_save_data_drift_report()
            self.save_data_drift_report()
            return True
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.column_name_check()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path = self.data_validation_config.report_page_file_path,
                is_validated=True,
                message='Data Validation performed Successfully'
            )
            logging.info(f"Data Validation Artifact:{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*30}Data Valdaition log completed.{'<<'*30} \n\n")