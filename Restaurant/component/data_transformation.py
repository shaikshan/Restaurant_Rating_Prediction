from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.entity.config_entity import DataTransformationConfig
from Restaurant.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
import os,sys

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