from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.component.data_ingestion import DataIngestion 
from Restaurant.config.configuration import Configuration
import os,sys
from Restaurant.entity.artifact_entity import DataIngestionArtifact


class Pipeline:
    def __init__(self,config:Configuration=Configuration()) -> None:
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

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise RestaurantException(e,sys) from e