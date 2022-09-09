
from datetime import datetime
import os,sys

ROOT_DIR = os.getcwd()

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

#SCHEMA FILE PATH
SCHEMA_DIR = "config"
SCHEMA_FILE_NAME = "schema.yaml"
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR,SCHEMA_DIR,SCHEMA_FILE_NAME)


CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

#TRAINING_PIPELINE_KEYS
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"
TRAINING_ARTIFACT_DIR_KEY = "artifact_dir"

#DATA_INGESTION_KEYS
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATASET_DOWNLOAD_URL_KEY = "dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_ZIP_DOWNLOAD_DIR_KEY = "zip_download_dir"
DATA_INGESTION_INGESTED_DIR_KEY = "ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DATA_KEY = "ingested_train_data"
DATA_INGESTION_INGESTED_TEST_DATA_KEY = "ingested_test_data"
#DATA_VALIDATION_KEYS

DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"
DATA_VALIDATION_ARTIFACT_DIR_NAME = 'data_validation'


#DATA TRANSFORMATION_KEYS

DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"
DATA_TRANSFORMATION_DIR_NAME_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY = "transformed_train_dir"
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY = "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSING_FILE_NAME_KEY = "preprocessed_object_file_name"


NUMERICAL_COLUMNS_KEY = "numerical_columns"
CATEGORICAL_COLUMNS_KEY = "categorical_columns"

TARGET_COLUMN_KEY = "target_column"

DATASET_SCHEMA_COLUMNS_KEY = 'columns'

#MODEL TRAINER


MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = "model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY = "model_config_file_name"


#MODEL EVALUATION 
MODEL_EVALUATION_CONFIG_KEY = "model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY = "model_evaluation_file_name"
MODEL_EVALUATION_ARTIFACT_DIR = "model_evaluation"

BEST_MODEL_KEY = 'best_model'
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"

#MODEL PUSHER
MODEL_PUSHER_CONFIG_KEY = "model_pusher_config"
MODEL_PUSHER_EXPORT_DIR_KEY = "model_export_dir"

EXPERIMENT_DIR_NAME = "experiment"
EXPERIMENT_FILE_NAME = "experiment.csv" 