from Sensor.exception import SensorException
from Sensor.utils import get_collection_as_dataframe
import sys,os
from Sensor.entity.config_entity import DataIngestionConfig
from Sensor.entity import config_entity
from Sensor.components.DataIngestion import DataIngestion
from Sensor.components.DataValidation import DataValidation
from Sensor.components.DataTransformation import DataTransformation
from Sensor.components.ModelTrainer import ModelTrainer
from Sensor.components.ModelEvaluation import ModelEvaluation

if __name__=="__main__":
     try:
          training_pipeline_config=config_entity.TrainingPipelineConfig()
          
          # Data_Ingestion_Starting
          data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config)
          data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
          
          #Data_Validation_starting
          data_validation_config=config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
          data_validation_arifact=data_validation.initiate_data_validation()

          #data_Transformation_Starting
          data_transformation_config=config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation=DataTransformation(data_transformation_config=data_transformation_config,
          data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact=data_transformation.initiate_data_transformation()

          #Model Training 
          model_trainer_config=config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,
           data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact=model_trainer.initiate_model_trainer()

          #Model Evaluation
          model_evaluation_config=config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_evaluation=ModelEvaluation(model_evaluation_config=model_evaluation_config, data_transformation_artifact=data_transformation_artifact,
           data_ingestion_artifact=data_ingestion_artifact, model_trainer_artifact=model_trainer_artifact)
          model_evaluation.initiate_model_evaluation()

     except Exception as e:
          raise SensorException(e, sys)
