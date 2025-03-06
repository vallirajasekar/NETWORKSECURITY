from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.expection.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig

import sys


if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info('Initiating the Data Ingestion')
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info('Data Ingestion is completed')
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("initiate data Vlaidation")
        datavalidationartifact=data_validation.initiate_data_validation()
        logging.info("Data validation Completed")
        print(datavalidationartifact)



        

    except Exception as e:
        raise NetworkSecurityException(e,sys)

