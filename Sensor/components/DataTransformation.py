from Sensor.entity import artifact_entity,config_entity
from Sensor.logger import logging
from  Sensor.exception import SensorException
import sys,os
from Sensor import utils
import pandas as pd
from Sensor.entity.config_entity import DataIngestionConfig
import numpy as np
from typing import Optional
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from Sensor.config import TARGET_COLUMN
from imblearn.combine import SMOTETomek

class DataTransformation():
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f" {'>>'*10}Data Transformation{'<<'*10}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)

    @classmethod
    def get_transformer_object(cls)->Pipeline:
        try:
            simple_imputer=SimpleImputer(strategy="constant",fill_value=0)
            robust_scaler=RobustScaler()
            pipeline=Pipeline(steps=[("Imputer",simple_imputer),("Robust Scaler",robust_scaler)])
            return pipeline
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)

    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        try:
            logging.info(f"Now Reading the Train and Test Dataset from Data IngestionArtifact")
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #storing input feature and target feature separately
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_test_df=test_df[TARGET_COLUMN]

            #Firstly we are fitting the LabelENcoder
            label_encoder=LabelEncoder()
            target_feature_train_arr=label_encoder.fit(target_feature_train_df)
            
            # Now we are Transforming the LabelEncoder
            target_feature_train_arr=label_encoder.transform(target_feature_train_df)
            target_feature_test_arr=label_encoder.transform(target_feature_test_df)

            #Transforming Input Features
            transformation_pipeline=DataTransformation.get_transformer_object()
            transformation_pipeline.fit(input_feature_train_df )

            #Transforming Input Train and test Features
            transfomed_input_train_arr=transformation_pipeline.transform(input_feature_train_df)
            transfomed_input_test_arr=transformation_pipeline.transform(input_feature_test_df)

            smt=SMOTETomek(random_state=11)
            logging.info(f"Before Sampling Shape of Transformed Train Input:{transfomed_input_train_arr.shape} and Transformed Train Target: {target_feature_train_arr.shape} ")
            transformed_input_train_arr,transformed_target_train_arr=smt.fit_resample(transfomed_input_train_arr,target_feature_train_arr)
            logging.info(f"Before Sampling Shape of Transformed Train Input:{transfomed_input_train_arr.shape} and Transformed Train Target: {target_feature_train_arr.shape} ")
            
            logging.info(f"Before Sampling Shape of Transformed Test Input :{transfomed_input_test_arr.shape} and Transformed Test Target: {target_feature_test_arr.shape} ")
            transformed_input_test_arr,transformed_target_test_arr=smt.fit_resample(transfomed_input_test_arr,target_feature_test_arr)
            logging.info(f"Before Sampling Shape of Transformed Test Input :{transfomed_input_test_arr.shape} and Transformed Test Target: {target_feature_test_arr.shape} ")

            #Concatenaing INput and Target Feature of Train and test data
            train_arr=np.c_[transformed_input_train_arr,transformed_target_train_arr]
            test_arr=np.c_[transformed_input_test_arr,transformed_target_test_arr]

            #Saving Numpy Array Data
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,
            array_data=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,
            array_data=test_arr)

            #Saving Transformer Objects
            utils.save_object(file_path=self.data_transformation_config.data_transformed_object_path, obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path, obj=label_encoder)
            
            data_transformation_artifact=artifact_entity.DataTransformationArtifact(
                transformed_object_path=self.data_transformation_config.data_transformed_object_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path, 
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path)
            logging.info(f"Returning the Data Transformation Artifact :{data_transformation_artifact}")
            return data_transformation_artifact 

        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)
