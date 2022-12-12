import pandas as pd 
from Sensor.logger import logging
from Sensor.exception import SensorException
from Sensor.entity import config_entity,artifact_entity
from Sensor.config import  MongoClient
import os,sys
import yaml
from typing import Optional


def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description :
    This Function returns Data as DataFrame
    database_name:Name of Database
    collection_name:Name of Collection

    returns Pandas Dataframe
    """
    
    try:
        logging.info(f"Reading Data From Database : {database_name} and Collection : {collection_name}")
        df=pd.DataFrame(list(MongoClient[database_name][collection_name].find()))
        logging.info(f"Found Columns{df.columns}")
        if "_id" in df.columns:
            df=df.drop("_id",axis=1)
            logging.info("Dropping the Column _id")
        logging.info(f"Row and COlumns:{df.shape}")
        return df
    except Exception as e:
        raise SensorException(e,sys)
    
def write_yaml_file(file_path:str,data:dict):
    try :
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)

    except Exception as e:
        raise SensorException(e, sys)

def convert_column_to_float(df:pd.DataFrame,exclude_column_names:list)-> pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_column_names:
                df[column]=df[column].astype("float")
        return df
    except Exception as e:
        raise SensorException(error_message=e, error_detail=sys)