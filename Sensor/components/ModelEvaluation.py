from Sensor.predictor import ModelResolver
from Sensor.entity import config_entity,artifact_entity
from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.utils import load_object
import pandas as pd 
from Sensor.config import TARGET_COLUMN
from sklearn.metrics import f1_score


class ModelEvaluation:
    def __init__(self,
        model_evaluation_config:config_entity.ModelEvaluationConfig,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
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
            logging.info("if saved model dir has model only then we can compare \
            which model is better")
            if latest_dir_path ==None:
                model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improve_Accuracy=None)
                logging.info(f"Model Evaluation Artifact :{model_eval_artifact}")
                return model_eval_artifact
            
            #Finding location of model_path,transformer_path and target_encoder_path
            model_path=self.model_resolver.get_latest_model_path()
            transformer_path=self.model_resolver.get_latest_transformer_path()
            target_encoder_path=self.model_resolver.get_latest_target_encoder_path()
            logging.info(f"now checking for the LOcation of {model_path},{transformer_path},{target_encoder_path}")
            
            #Previous trained object
            model=load_object(file_path=model_path)
            transfomer=load_object(file_path=transformer_path)
            target_encoder=load_object(file_path=target_encoder_path)

            #Current Trained Objects
            current_model=load_object(file_path=self.model_trainer_artifact.model_path)
            current_transformer=load_object(file_path=self.data_transformation_artifact.transformed_object_path)
            current_target_encoder=load_object(file_path=self.data_transformation_artifact.target_encoder_path)
            logging.info(f"now checking for the LOcation of current Model {current_model_path},{current_transformer_path},\
            {current_target_encoder_path}")

            logging.info("reading test_Data to check the accuracy")
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_column=test_df[TARGET_COLUMN]            
            y_true=target_encoder_path.transform(target_column)

            logging.info(" Accuracy using Previous Model")
            input_arr=transfomer.transform(test_df)
            prediction = model.predict(input_arr)
            print(f"Prediction using previous models: {target_encoder.inverse_transform(prediction[:5])}")
            previous_model_score=f1_score(y_true=y_true,y_pred=prediction)
            logging.info(f"Accuracy using Current model : {previous_model_score}")
            print(f"Accuracy using Previous Models : {f1_score(y_true=y_true,y_pred=prediction)}")
            
            logging.info(" Accuracy using Current Model")
            input_arr=current_transformer.transform(test_df)
            current_prediction=current_model.predict(input_arr)
            print(f"Prediction using current models: {current_target_encoder.inverse_transform(current_prediction[:5])}")
            current_model_score=f1_score(y_true=y_true,y_pred=current_prediction)
            logging.info(f"Accuracy using Current model : {current_model_score}")
            print(f"Accuracy using current Models : {f1_score(y_true=y_true,y_pred=current_prediction)}")

            if current_model_score<previous_model_score:
                logging.info(f"Current Model is not Better")
                raise Exception(f"Current Model is not better than Previous Model")
            
            model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, 
            improve_Accuracy=(current_model_score-previous_model_score))

            logging.info(f"Model Eval Artifact:{model_eval_artifact}")


        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)
    
