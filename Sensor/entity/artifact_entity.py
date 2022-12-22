from dataclasses import dataclass
 
@dataclass
class DataIngestionArtifact:
    feature_store_dir:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass    
class DataTransformationArtifact:
    transformed_object_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str
    f1_test_score:float
    f1_train_score:float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    model_Accuracy:float
                                                                               
class ModelPusherArtifact:... 
