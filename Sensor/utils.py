import pandas as pd 
from Sensor.logger import logging
from Sensor.exception import SensorException
from Sensor.entity import config_entity,artifact_entity
from Sensor.config import  MongoClient
import os,sys
import yaml
from typing import Optional
import dill
import numpy as np


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
        logging.info(f"{MongoClient[database_name][collection_name]}")

        df=pd.DataFrame(list(MongoClient[database_name][collection_name].find()))
        logging.info(f"{df.shape}")
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

def save_object(file_path:str,obj:object):
    try:
        logging.info(f"Entered the save_object method of mainutils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info(f"exiting the Save_object method of mainutil class")

    except Exception as e :
        raise SensorException(error_message=e, error_detail=sys)
def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"File {file_path } does not Exist")
        with open(file_path,"rb") as file:

            file_obj=dill.load(file)
        return file_obj 
    except Exception as e :
        raise SensorException(error_message=e, error_detail=sys)
    
def save_numpy_array_data(file_path:str,array_data:np.array):
    """
    Save Numpy Array Data 
    Arguments Requires:
    1.Path where you want to save the Numpy_array_data
    2. Array Data which you want to save


    """
    try: 
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_object:
            np.save(file_object,array_data)

    except Exception as e :
        raise SensorException(error_message=e, error_detail=sys)

def load_numpy_array_data(file_path:str):
    try:
        if not os.path.exists(file_path):
            return Exception(f"Sorry but File {file_path} does not Exist")

        with open(file_path,"rb") as file_object:
            numpy_array_data=dill.load(file_object)
        return numpy_array_data
    except Exception as e :
        raise SensorException(error_message=e, error_detail=sys)

        