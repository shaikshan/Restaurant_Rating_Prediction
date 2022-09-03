from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.component.data_ingestion import DataIngestion 
from Restaurant.config.configuration import Configuration
import os,sys
from Restaurant.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from Restaurant.component.data_validation import DataValidation
from Restaurant.component.data_transformation import DataTransformation
from Restaurant.component.model_trainer import ModelTrainer

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

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact,
                                        data_ingestion_artifact:DataIngestionArtifact)->DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                            data_transformation_config=self.config.get_data_transformation_config(),
                                            data_ingestion_artifact=data_ingestion_artifact)
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact,)->ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                                data_transformation_artifact=data_transformation_artifact)
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                            data_validation_artifact=data_validation_artifact)
            model_trainer = self.start_model_training(data_transformation_artifact=data_transformation_artifact)

            return model_trainer
        except Exception as e:
             raise RestaurantException(e,sys) from e