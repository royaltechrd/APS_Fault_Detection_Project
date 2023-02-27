from Sensor.predictor import ModelResolver
from Sensor.entity.config_entity import ModelPusherConfig
from Sensor.entity.artifact_entity import DataTransformationArtifact,ModelPusherArtifact,ModelTrainerArtifact
from Sensor.exception import exception
from Sensor.logger import logging
import os, sys
from Sensor.utils import load_object,save_object


class ModelPusher:
    
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
        model_pusher_artifact:ModelPusherArtifact,
        model_trainer_artifact:ModelTrainerArtifact):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_artifact=model_trainer_artifact
        self.model_pusher_artifact=model_pusher_artifact

    def iniatiate_model_pusher(self)->ModelPusherArtifact:
        modelresolver=ModelResolver()
        # Load the Object
        model=load_object(self.model_trainer_artifact.model_path)
        transfomer=load_object(self.data_transformation_artifact.transformed_object_path)
        target_encoder=load_object(self.data_transformation_artifact.target_encoder_path)

        #model_pusher dir
        save_object(file_path=self.model_trainer_artifact.model_path, obj=model)
        save_object(file_path=self.data_transformation_artifact.transformed_object_path, obj=transfomer)
        save_object(file_path=self.data_transformation_artifact.target_encoder_path, obj=target_encoder)
        
        # Saved  model dir
        save_object(file_path=modelresolver.get_latest_save_model_path(), obj=model)
        save_object(file_path=modelresolver.get_latest_save_target_encoder_path(), obj=target_encoder)
        save_object(file_path=modelresolver.get_latest_save_model_path(), obj=transfomer)

