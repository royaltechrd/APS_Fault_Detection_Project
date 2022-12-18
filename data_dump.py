import pymongo
import pandas as pd
import json

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH='/config/workspace/aps_failure_training_set1.csv'
DATABASE_NAME='APS'
COLLECTION_NAME='SENSOR'

if __name__ =='__main__' :
    data=pd.read_csv(DATA_FILE_PATH)
    print(f"ROWS and Column : {data.shape}")

    #Convert Df to json so that we can dump these records in Mongo DB
    data.reset_index(drop=True,inplace=True)
    # Now convert CSV data to Json for Uploading it to MongoDB Dataset 
    jsonData=list(json.loads(data.T.to_json()).values())

    client[DATABASE_NAME][COLLECTION_NAME].insert_many(jsonData)
