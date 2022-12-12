import os 
from Sensor.exception import SensorException
from datetime import datetime
from Sensor.entity import config_entity
import sys
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
SENSOR="sensor.csv"

class TrainingPipelineConfig():
    def __init__(self):
        self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class DataIngestionConfig():
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name="APS"
            self.collection_name="SENSOR"
            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,"Data Ingeston")
            self.feature_store_dir=os.path.join(self.data_ingestion_dir,"feature Store",SENSOR)
            self.test_file_path=os.path.join(self.data_ingestion_dir,"Datasets",TEST_FILE_NAME)
            self.train_file_path=os.path.join(self.data_ingestion_dir,"Datasets",TRAIN_FILE_NAME)
            self.test_size=0.2
        except Exception as e:
            raise SensorException(e,sys)


    def to_dict(self)->dict:
        try:
            return self.__dict__
        
        except Exception as e:
            raise SensorException(e,sys)


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig()):
        self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,"Data Validation")
        self.report_file_path=os.path.join(self.data_validation_dir,"Report.yaml")
        self.missing_values:float=0.2
        self.base_file_path=os.path.join("aps_failure_training_set1.csv")
        
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
