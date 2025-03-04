import os 
import sys
import json 

from dotenv import load_dotenv
load_dotenv()

MANGO_DB_URL=os.getenv("MANGODB_URL")
print(MANGO_DB_URL)

import pandas as pd 
import numpy as np
import pymongo
from NetworkSecurity.expection.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging 


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mangodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mango_client=pymongo.MongoClient(MANGO_DB_URL)
            self.database=self.mango_client[self.database]

            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    FILE_PATH="Network Data/phisingData.csv"
    DATABASE="VALLI_ML"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mangodb(records,DATABASE,Collection)
    print(no_of_records)
