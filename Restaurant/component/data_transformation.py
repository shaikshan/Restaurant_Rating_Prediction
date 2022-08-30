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

    def get_preprocessing_object(self):
        try:
            pass
        except Exception as e:
            raise RestaurantException(e,sys) from e

    