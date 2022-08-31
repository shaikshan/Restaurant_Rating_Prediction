from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.component.data_ingestion import DataIngestion 
from Restaurant.config.configuration import Configuration
import os,sys
from Restaurant.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Restaurant.component.data_validation import DataValidation

class Pipeline:
    def __init__(self,config:Configuration=Configuration()):
        try:
            self.config = config
        except Exception as e:
            raise RestaurantException(e,sys) from e
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = DataValidation(data_ingestion_artifact= data_ingestion_artifact,
                                data_validation_config=self.config.get_data_validation_config())
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            return data_validation_artifact
        except Exception as e:
            raise RestaurantException(e,sys) from e