from Sensor.entity import artifact_entity,config_entity
from Sensor.logger import logging
from  Sensor.exception import SensorException
import sys,os
from Sensor import utils
import pandas as pd
import numpy as np
from typing import Optional
from xgboost import XGBClassifier
from sklearn.metrics import f1_score

class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
    data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*10}Model Trainer {'<<'*10}'")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)
    
    def train_model(self,x,y):
        try:
            xg_clf=XGBClassifier()
            logging.info(f"Starting to Train the Model : {xg_clf}")
            xg_clf.fit(x,y)
            return xg_clf
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)
    def fine_tune(self):
        try:
            ...
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)

    def initiate_model_trainer(self)-> artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Starting to Loading the Train and test array from the utils class")
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            #Remember this line of code is for array slice 
            # and while if var is pd.DataFrame then we need to use iloc

            x_train,y_train=train_arr[:,:1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:1],test_arr[:,-1]

            model=self.train_model(x=x_train,y=y_train)
            logging.info(f"Now starting to predict the y of Train and test array")
            yhat_train=model.predict(x_train)
            
            f1_train_score=f1_score(y_true=y_train,y_pred=yhat_train)
            #Here why we are using the f1_score because we want the Harmonic mean of Precision and recall for this Project 
            # It can be decided on the basis of Requirement of the Project 
            # In General , we use R1_score for the Regression and use f1_score for the Classification

            yhat_test=model.predict(x_test)
            f1_test_score=f1_score(y_true=y_test,y_pred=yhat_test)
            
            logging.info(f"Train Score : {f1_train_score} and Test Score :{f1_test_score}")
            #Check for underfitting or Overfitting or expected_score
            logging.info(f"Check whether the Model is underfitted or not ")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give / expected accuracy :\
                     {self.model_trainer_config.expected_score}; Model actual Score : {f1_test_score}")

            logging.info(f"Check whether the Model is overfitted or not ")
            diff=abs(f1_test_score-f1_train_score)
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and Test score Difference : {diff} \
                    is more than the Overfitting Threshold :{self.model_trainer_config.overfitting_threshold}")
            
            #Saving the Train Model Object
            logging.info(f"Saving the Model :{model } to the Model Trainer Config of model path")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)
            
            #Prepare the Artifact 
            model_trainer_artifact=artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
             f1_test_score=f1_test_score, f1_train_score=f1_train_score)
            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")
            return model_trainer_artifact


        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)