from tkinter import E
from unicodedata import category

from sklearn import preprocessing
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






class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                data_ingestion_artifact:DataIngestionArtifact,
                data_validation_artifact:DataValidationArtifact):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_preprocessing_object(self):
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMNS_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMNS_KEY]

            num_pipeline = Pipeline(steps=[('imputer',SimpleImputer(strategy='median')),
                                    ('scaler',StandardScaler())])

            cat_pipeline = Pipeline(steps=[('impute',SimpleImputer(strategy="most_frequent")),
                                        ('one_hot_encoder',OneHotEncoder()),
                                        ('scaler',StandardScaler(with_mean=False))])
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessing = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns),
            ])

            return preprocessing
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            logging.info(f"Loading train_df,and test_df")

            train_df['approx_cost(for two people)'] = train_df['approx_cost(for two people)'].str.replace(",","")
            train_df['approx_cost(for two people)'] = pd.to_numeric(train_df['approx_cost(for two people)'])
            logging.info(f"changing approx column into float")

            test_df['approx_cost(for two people)'] = test_df['approx_cost(for two people)'].str.replace(",","")
            test_df['approx_cost(for two people)'] = pd.to_numeric(test_df['approx_cost(for two people)'])
            logging.info(f"changing approx column into float")

            train_df['online_order'] = train_df['online_order'].astype('category')
            train_df['book_table']= train_df['book_table'].astype('category')
            logging.info(f"changing dtype of online_order,book_table into category")

            
            test_df['online_order'] = test_df['online_order'].astype('category')
            test_df['book_table']= test_df['book_table'].astype('category')
            logging.info(f"changing dtype of online_order,book_table into category")

            train_df['dish_liked'] = train_df['dish_liked'].apply(count)
            train_df['cuisines'] = train_df['cuisines'].apply(count)
            logging.info(f"changing dish_liked,cuisines into int64 by decoding it into numbers")

            test_df['dish_liked'] = test_df['dish_liked'].apply(count)
            test_df['cuisines'] = test_df['cuisines'].apply(count)
            logging.info(f"changing dish_liked,cuisines into int64 by decoding it into numbers")

            train_df = load_data(dataframe=train_df,schema_file_path=schema_file_path)

            test_df = load_data(dataframe=test_df,schema_file_path=schema_file_path)

            #columns remove
            columns = ['name','location','rest_type','listed_in(type)','listed_in(city)']

            train_df = columns_removal(columns=columns,df=train_df)
            logging.info(f"Removing columns of list:{columns}")

            test_df = columns_removal(columns=columns,df=test_df)
            logging.info(f"Removing columns of list:{columns}")

            #Outliers removing
            train_df = cap_data(df=train_df)
            logging.info("Removing Outliers test_df")

            test_df = cap_data(df=test_df) 
            logging.info("Removing Outliers of test_df")
            
            #Filling nan values
            # med = round(train_df['approx_cost(for two people)'].median(skipna=True))
            # logging.info(f"Filling values in approx column of train_df with median:{med}")

            # train_df['approx_cost(for two people)'] = train_df['approx_cost(for two people)'].apply(fill_na,args=(med))


            # test_med = round(test_df['approx_cost(for two people)'].median(skipna= True))
            # logging.info(f"Filling nan values in approx column of test_df with median:{test_med}")

            preprocessing_obj = self.get_preprocessing_object()

            schema = read_yaml_file(file_path=schema_file_path)
            
            target_column_name = schema[TARGET_COLUMN_KEY]

            logging.info(f"Splitting input and target feature from training and testing dataframe")
            input_features_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_features_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_features_train_arr = preprocessing_obj.fit_transform(input_features_train_df)
            input_features_test_arr = preprocessing_obj.transform(input_features_test_df)

            train_arr = np.c_[input_features_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_features_test_arr,np.array(target_feature_test_df)]
            
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir
                        
            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            
            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")

            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
 
            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
            message="Data transformation successfull.",
            transformed_train_file_path=transformed_train_file_path,
            transformed_test_file_path=transformed_test_file_path,
            preprocessed_object_file_path=preprocessing_obj_file_path

            )
            logging.info(f"Data transformationa artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise RestaurantException(e,sys) from e

            
    def __del__(self):
        logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")




    