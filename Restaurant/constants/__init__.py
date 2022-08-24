
from datetime import datetime
import os,sys

from Restaurant.logger import CURRENT_TIME_STAMP
ROOT_DIR = os.getcwd()

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%M-%d-%H-%M:%S')}"

#TRAINING_PIPELINE_KEYS
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"
TRAINING_ARTIFACT_DIR_KEY = "artifact_dir"

#DATA_INGESTION_KEYS
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_DOWNLOAD_URL_KEY = "data_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY = "tgz_download__dir"
DATA_INGESTION_INGESTED_DIR_KEY = "ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DATA_KEY = "ingested_train_data"
DATA_INGESTION_INGESTED_TEST_DATA_KEY = "ingested_test_data    "

#DATA_VALIDATION_KEYS

DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
SCHEMA_DIR_KEY = "schema_dir"
SCHEMA_FILE_NAME_KEY = "schema_file_name"
REPORT_FILE_NAME_KEY = "report_file_name"
REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"

