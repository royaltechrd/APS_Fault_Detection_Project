from Sensor.entity import artifact_entity,config_entity
from Sensor.logger import logging
from  Sensor.exception import SensorException
from scipy.stats import ks_2samp
import sys,os
from Sensor import utils
import pandas as pd
from Sensor.entity.config_entity import DataValidationConfig
import numpy as np
from typing import Optional
# Optional is basically shows it will contain this DataType or None
# SImilar function like OPtional is Union that shows it contain all the types that are given like Union['int',"str","float"]

class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,
                data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20}Data Validation{'<<'*20}")
            self.data_validation_config=data_validation_config
            self.validation_error=dict()
            self.data_ingestion_artifact=data_ingestion_artifact
            
        except Exception as e:
            raise SensorException(e, sys)
    def is_required_column_exist(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            logging.info(f"Checking Columns Exist or not for base df")
            base_columns=base_df.columns
            current_columns=current_df.columns
            missing_columns=[]
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column{base_column} is not available in Training dataset")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False
            return True
        except Exception as e:
            raise SensorException(e, sys)


    def drop_missing_value_columns(self,df:pd.DataFrame,report_key_name:str) -> Optional[pd.DataFrame]:

        """
        This Function Return None or Pandas Dataframe if missing values of a Column is greater than a Specific Value
        df: Pandas Dataframe
        ============================================================================================================
        returns Pandas DataFrame or None.

        """
        try:

            logging.info("Dropping the Columns having Missing values more than the Threshold Values")
            threshold=self.data_validation_config.missing_values
            null_report=df.isnull().sum()/df.shape[0]
            
            #selecting column which has more than the threshold
            drop_columns_names=df[null_report[null_report>threshold].index]
            logging.info(f"Following columns {list(drop_columns_names)} which has more than the threshold")
            df.drop(list(drop_columns_names),axis=1,inplace=True)
            self.validation_error[report_key_name]=list(drop_columns_names)
            
            # return None if no column is left
            if len(df.columns)==0:
                return None
            else:
                return df

        except Exception as e:
            raise SensorException(e,sys)

    def data_drift(self ,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):

        try:
            logging.info(f"Now checking for any Data Drift in the Training dataset with respect to Base Dataset")
            drift_report=dict()
            base_columns=base_df.columns
            current_columns=current_df.columns
            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]
                same_distribution=ks_2samp(base_data,current_data)
                logging.info(f"Hypothese:{base_column}:{base_data.dtype},{current_data.dtype}")
                # NUll hypothesis is that Both data have the same Distribution

                if same_distribution.pvalue>0.05:
                    drift_report[base_column]={"pvalues":float(same_distribution.pvalue),"Same_distribution":True}
                #same distribution
                else:
                    drift_report[base_column]={"pvalues":float(same_distribution.pvalue),"Same_Distribution":False}
                    #different Distribution
            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise SensorException(e, sys)
            ...
   
    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading the BAse data from {self.data_validation_config.base_file_path}")
            base_df=pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na" : np.NAN},inplace=True)
            
            # base_df has na as null as per the EDA Report
            logging.info(f"Now removing Null Column from base dataset")
            base_df=self.drop_missing_value_columns(base_df,report_key_name="Missing_values_within_Base_dataset")
            
            #Reading train and test csv from dataingestion output
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Now removing Null Columns values from Training and Testing dataset")
            train_df_column_status=self.drop_missing_value_columns(train_df,report_key_name="Missing_values_within_training dataset")
            test_df_column_status=self.drop_missing_value_columns(test_df,report_key_name="Missing_values_within_Testing data")

            exclude_column_names=['class']
            base_df=utils.convert_column_to_float(df=base_df, exclude_column_names=exclude_column_names)
            train_df=utils.convert_column_to_float(df=train_df, exclude_column_names=exclude_column_names)
            test_df=utils.convert_column_to_float(df=test_df, exclude_column_names=exclude_column_names)

            logging.info(f"is required column exist in train_df")
            train_df_column_status=self.is_required_column_exist(base_df=base_df, current_df=train_df, report_key_name="is required column exist")
            logging.info(f"is required column exist in test_df")
            test_df_column_status=self.is_required_column_exist(base_df=base_df, current_df=train_df, report_key_name="is required column exist")

            if train_df_column_status:
                logging.info(f"as all column are available in Train df now detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df, report_key_name=" Data Drift within Trainng Dataset")
            if test_df_column_status:
                logging.info(f"as all column are available in test df now detecting data drift")

                self.data_drift(base_df=base_df, current_df=test_df, report_key_name=" Data Drift within Testing Dataset")
            
            #Write yaml report 
            logging.info(f"Write Yaml Report")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path, data=self.validation_error)
            data_validation_artifact=artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f"Now returning {data_validation_artifact}")
            return data_validation_artifact


        except Exception as e:
            raise SensorException(e,sys)