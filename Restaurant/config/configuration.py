
from Restaurant.constants import CONFIG_FILE_NAME
from Restaurant.logger import logging
from Restaurant.exception import RestaurantException
import os,sys
from Restaurant.entity.config_entity import *
from Restaurant.constants import *
from Restaurant.util.util import *
class Configuration:
    def __init__(self,
        config_file_path:str = CONFIG_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP)->None:
        try:
            self.config_info = read_yaml_file(file_path = config_file_path)
            self.time_stamp = current_time_stamp
            self.training_pipeline_config = self.get_training_pipeline_config()
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            data_ingestion_config_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            dataset_download_url = data_ingestion_config_info[DATA_DOWNLOAD_URL_KEY]
            zip_download_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_ZIP_DOWNLOAD_DIR_KEY])

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

            ingested_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_DIR_KEY])

            ingested_train_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DATA_KEY])
            
            ingested_test_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DATA_KEY])

            data_ingestion_config = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                tgz_download_dir=zip_download_dir,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )

            logging.info(f"Data ingestion config:{data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_ARTIFACT_DIR_KEY]
            )
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training Pipeline Config:{training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise RestaurantException(e,sys) from e