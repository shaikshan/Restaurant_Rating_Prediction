from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from Restaurant.entity.config_entity import ModelTrainerConfig
import os,sys


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                        data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*30}Model_Training_Start{'<<'*30}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise RestaurantException(e,sys) from e
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            pass
        except Exception as e:
            raise RestaurantException(e,sys) from e
    def __del__(self):
        try:
            logging.info(f"{'>>'*30}Model_Training_End{'<<'*30}")
        except Exception as e:
            raise RestaurantException(e,sys) from e