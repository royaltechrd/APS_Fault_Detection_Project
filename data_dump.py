import pymongo
import pandas as pd

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH='/config/workspace/aps_failure_training_set1.csv'
DATABASE_NAME='APS'
COLLECTION_NAME='SENSOR'

if _name_=='_main_' :
    data=pd.read_csv(DATA_FILE_PATH)
    print("ROWS and Column : {data.shape}")