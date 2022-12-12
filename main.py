from Sensor.exception import SensorException
from Sensor.utils import get_collection_as_dataframe
import sys,os
from Sensor.entity.config_entity import DataIngestionConfig
from Sensor.entity import config_entity
from Sensor.components.DataIngestion import DataIngestion
from Sensor.components.DataValidation import DataValidation

if __name__=="__main__":
     try:
          training_pipeline_config=config_entity.TrainingPipelineConfig()
          
          # Data_Ingestion_Starting
          data_ingestion_config=DataIngestionConfig(training_pipeline_config)
          data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
          
          #Data_Validation_starting
          data_validation_config=config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
          data_validation_arifact=data_validation.initiate_data_validation()

     except Exception as e:
          raise SensorException(e, sys)
