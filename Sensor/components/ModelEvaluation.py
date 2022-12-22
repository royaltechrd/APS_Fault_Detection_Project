from Sensor.predictor import ModelResolver
from Sensor.entity import config_entity,artifact_entity
from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.utils import load_object

class ModelEvaluation:
    def __init__(self,
        model_evaluation_config:config_entity.ModelEvaluationConfig,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        model_trainer_artifact:artifact_entity.ModelEvaluationArtifact):
        try:
            logging.info(f"{'>>'*15}Model Evaluaion Starting{'<<'*15}")
            self.model_evaluation_config=model_evaluation_config
            self.data_transformation_artifact=data_transformation_artifact
            self.data_ingestion_artifact=data_ingestion_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver=ModelResolver()
        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path=self.model_resolver.get_latest_dir_path()
            if latest_dir_path ==None:
                model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, model_Accuracy=None)
                logging.info(f"Model Evaluation Artifact :{model_eval_artifact}")
                return model_eval_artifact
        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)
    
