from sklearn import pipeline
from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.entity.config_entity import ModelEvaluationConfig
from Restaurant.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact, ModelTrainerArtifact,ModelEvaluationArtifact
import os,sys
from Restaurant.util.util import *
from Restaurant.constants import *
import numpy as np
import pandas as pd
from Restaurant.entity.model_factory import evaluate_regression_model
from Restaurant.Cleaning.Autoclean import Autoclean

class ModelEvaluation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                    data_validation_artifact:DataValidationArtifact,
                    data_transformation_artifact:DataTransformationArtifact,
                    model_evaluation_config:ModelEvaluationConfig,
                        model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*30} ModelEvaluation__Started {'<<'*30}")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_aritfact = data_transformation_artifact
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise RestaurantException(e,sys) from e
            
    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluated_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path)

                return model
            model_eval_file_content = read_yaml_file(file_path=model_evaluation_file_path)

            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY not in model_eval_file_content:
                return model
            
            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def update_evaluation_report(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            eval_file_path = self.model_evaluation_config.model_evaluated_file_path
            model_eval_file_content = read_yaml_file(file_path=eval_file_path)
            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_file_content:
                previous_best_model = model_eval_file_content[BEST_MODEL_KEY]

            logging.info(f"Previos eval result:{model_eval_file_content}")
            eval_result = {
                BEST_MODEL_KEY:{
                    MODEL_PATH_KEY:model_evaluation_artifact.evaluated_model_path,
                }
            }

            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp:previous_best_model}
                if HISTORY_KEY not in model_eval_file_content:
                    history  = {HISTORY_KEY:model_history}
                    eval_result.update(history)
                else:
                    model_eval_file_content[HISTORY_KEY].update(model_history)

            model_eval_file_content.update(eval_result)
            logging.info(f"Updated eval result:{model_eval_file_content}")
            write_yaml_file(file_path=eval_file_path,data = model_eval_file_content)

        except Exception as e:
            raise RestaurantException(e,sys) from e

    def initiate_model_evaluation(self):
        try:
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            trained_model_object = load_object(file_path=trained_model_file_path)

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            pipeline_ = Autoclean()

            train_dataframe = pipeline_.process(df=train_df,schema_path=schema_file_path)
            logging.info("Auto Cleaning and Validating training dataset")

            test_dataframe = pipeline_.process(df=test_df,schema_path=schema_file_path)
            logging.info("Auto Cleaning and validating testing dataset")

            schema_file_content = read_yaml_file(file_path=schema_file_path)
            target_column_name = schema_file_content[TARGET_COLUMN_KEY]

            #target column:
            logging.info(f"Converting target column into numpy array")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logging.info(f"Conversion completed target column into numpy array")

            #dropping target column from the dataframe 
            logging.info(f"Dropping target column from the dataframe")
            train_dataframe.drop(target_column_name,axis=1,inplace=True)
            test_dataframe.drop(target_column_name,axis=1,inplace=True)
            logging.info(f"Dropping target column from the dataframe completed.")

            model = self.get_best_model()

            if model is None:
                logging.info(f"Not found any existing model. Hence accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact=model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact{model_evaluation_artifact} created")
                return model_evaluation_artifact

            model_list = [model,trained_model_object]
            
            metric_info_artifact = evaluate_regression_model(model_list=model_list,
                                                                X_train = train_dataframe,
                                                                y_train=test_dataframe,
                                                                X_test=train_target_arr,
                                                                y_test=test_target_arr,
                                                                base_accuracy=self.model_trainer_artifact.model_accuracy)
            logging.info(f"Model evaluation completed. model metric artifact:{metric_info_artifact}")

            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted=False,
                                                evaluated_model_path=trained_model_file_path)
                logging.info(f"{response}")
                return response
            
            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=True,
                                                                    evaluated_model_path=trained_model_file_path)

                self.update_evaluation_report(model_evaluation_artifact=model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact}")
            
            else:
                logging.info(f"Trained Model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=False,
                                                                            evaluated_model_path=trained_model_file_path)

            return model_evaluation_artifact

        except Exception as e:
            raise RestaurantException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'>>'*30} ModelEvaluationCompleted {'<<'*30}")