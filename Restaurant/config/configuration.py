from Restaurant.logger import logging
from Restaurant.exception import RestaurantException
import os,sys
from Restaurant.entity.config_entity import *
from Restaurant.constants import *
from Restaurant.util.util import *
class Configuration:
    def __init__(self,
        config_file_path:str = CONFIG_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP
        )->None:
        try:
            self.config_info = read_yaml_file(file_path = config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
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

            dataset_info = data_ingestion_config_info[DATASET_INFO_KEY]
            zip_download_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_ZIP_DOWNLOAD_DIR_KEY])

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

            ingested_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_DIR_KEY])

            ingested_train_dir = os.path.join(ingested_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DATA_KEY])
            
            ingested_test_dir = os.path.join(ingested_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DATA_KEY])

            data_ingestion_config = DataIngestionConfig(
                dataset_info= dataset_info,
                zip_download_dir=zip_download_dir,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )

            logging.info(f"Data ingestion config:{data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir = os.path.join(artifact_dir,
            DATA_VALIDATION_ARTIFACT_DIR_NAME,
            self.time_stamp
            )
            data_validation_config_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            
            schema_file_path = os.path.join(ROOT_DIR,
            data_validation_config_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
            data_validation_config_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )

            report_file_path = os.path.join(data_validation_artifact_dir,
            data_validation_config_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY])

            report_page_file_path = os.path.join(data_validation_artifact_dir,
            data_validation_config_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])

            data_validation_config = DataValidationConfig(schema_file_path=schema_file_path,
                                    report_file_path=report_file_path,
                                    report_page_file_path=report_page_file_path)
            return data_validation_config
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_transformation_config_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            data_transformation_artifact_dir = os.path.join(artifact_dir,
            DATA_TRANSFORMATION_DIR_NAME_KEY,
            self.time_stamp)

            tranformed_train_dir = os.path.join(data_transformation_artifact_dir,
            data_transformation_config_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
            data_transformation_config_info[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY])

            transformed_test_dir = os.path.join(data_transformation_artifact_dir,
            data_transformation_config_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
            data_transformation_config_info[DATA_TRANSFORMATION_TEST_DIR_NAME_KEY])

            preprocessing_object_file_path = os.path.join(data_transformation_artifact_dir,
            data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
            data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_FILE_NAME_KEY])

            data_transformation_config = DataTransformationConfig(transformed_train_dir=tranformed_train_dir,
            transformed_test_dir=transformed_test_dir,
            preprocessed_object_file_path=preprocessing_object_file_path)
            logging.info(f"Data transformation config: {data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_model_trainer_config(self)->ModelTrainerConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            model_trainer_artifact_dir = os.path.join(artifact_dir,MODEL_TRAINER_ARTIFACT_DIR,
            self.time_stamp)

            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]

            trained_model_file_path = os.path.join(model_trainer_artifact_dir,
            model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY])

            model_config_file_path = os.path.join(
            model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY])

            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_trainer_config = ModelTrainerConfig(trained_model_file_path=trained_model_file_path,
            base_accuracy=base_accuracy,
            model_config_file_path=model_config_file_path)

            return model_trainer_config
        except Exception as e:
            raise RestaurantException(e,sys) from e
    
    def get_model_evaluation_config(self):
        try:
            model_evaluation_config_info = self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            model_evaluation_file_name = os.path.join(artifact_dir,
            MODEL_EVALUATION_ARTIFACT_DIR,
            model_evaluation_config_info[MODEL_EVALUATION_FILE_NAME_KEY])

            model_evaluation_config = ModelEvaluationConfig(model_evaluated_file_path=model_evaluation_file_name,
                                                            time_stamp=self.time_stamp)

            logging.info(f"ModelEvaluationConfig:{ model_evaluation_config}")
            return model_evaluation_config
        except Exception as e:
            raise RestaurantException(e,sys) from e
    def get_model_pusher_config(self)->ModelPusherConfig:
        try:
            time_stamp = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            model_pusher_config_info = self.config_info[MODEL_PUSHER_CONFIG_KEY]
            export_dir_path = os.path.join(ROOT_DIR,model_pusher_config_info[MODEL_PUSHER_EXPORT_DIR_KEY],
                                                time_stamp)

            model_pusher_config = ModelPusherConfig(export_dir_path=export_dir_path)
            logging.info(f"Model pusher config {model_pusher_config}")
            return model_pusher_config
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
