import pymongo
import pandas as pd
import json
from dataclasses import dataclass
import os


@dataclass()
class EnvironmentVariable:
    monog_db_url:str=os.getenv("MONGO_DB_URL")
    aws_access_key_id:str=os.getenv("AWS_ACCESS_KEYID")
    aws_secret_key_id:str=os.getenv("AWS_SECRET_ACCESS_KEY")

env_var=EnvironmentVariable()

# Provide the mongodb localhost url to connect python to mongodb.
MongoClient = pymongo.MongoClient(env_var.monog_db_url)

DATA_FILE_PATH='/config/workspace/aps_failure_training_set1.csv'
DATABASE_NAME='APS'
COLLECTION_NAME='SENSOR'
TARGET_COLUMN="class"