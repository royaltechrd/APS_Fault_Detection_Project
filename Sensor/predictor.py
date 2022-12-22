import os
from Sensor.entity.config_entity import TARGET_ENCODER_FILE_NAME,TRANSFORMER_OBJECT_FILE_NAME,MODEL_FILE_NAME
from Sensor.exception import SensorException
from Sensor.logger import logging
from glob import glob
from typing import Optional


class ModelResolver:
    def __init__(self,model_registry:str="saved models",
        transformer_dir_name:str="Transformer",
        target_encoder_name:str="Target Encoder",
        model_dir_name="model"):
        self.model_registry=model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transformer_dir_name=transformer_dir_name
        self.model_dir_name=model_dir_name
        self.target_encoder_name=target_encoder_name
    
    def get_latest_dir_path(self)->Optional[str]:
        try:
            dir_names=os.listdir(self.model_registry)
            if len(dir_names)==0:
                return None
            dir_names=list(map(int,dir_names))
            latest_dir_name=max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)

    def get_latest_model_path(self):
        try:
            dir_path=self.get_latest_dir_path()
            return os.path.join(dir_path,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)
    def get_latest_transformer_path(self):
        try:
            latest_dir_name=self.get_latest_dir_path()
            return os.path.join(latest_dir_name,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)
    def get_latest_target_encoder_path(self):
        try:
            latets_dir=self.get_latest_dir_path()
            return os.path.join(latets_dir,self.target_encoder_name,TARGET_ENCODER_FILE_NAME)
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)
    
    def get_latest_save_dir_path(self):
        try:
            last_dir_names=self.get_latest_dir_path()
            if last_dir_names == None:
                return os.path.join(self.model_registry,"0")
            last_dir_basename=int(os.path.basename(last_dir_names))
            return os.path.join(self.model_registry,f"{last_dir_basename+1}")

        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)

    def get_latest_save_model_path(self):
        try:
            dir_path=self.get_latest_save_dir_path()
            return os.path.join(dir_path,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)
    def get_latest_save_transformer_path(self):
        try:
            latest_dir_name=self.get_latest_save_dir_path()
            return os.path.join(latest_dir_name,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)
    def get_latest_save_target_encoder_path(self):
        try:
            latets_dir=self.get_latest_save_dir_path()
            return os.path.join(latets_dir,self.target_encoder_name,TARGET_ENCODER_FILE_NAME)
        except Exception as e :
            raise SensorException(error_message=e, error_detail=sys)

class Predictor:
    def __init__(self,model_resolver:ModelResolver):
        self.model_resolver=model_resolver
    



    