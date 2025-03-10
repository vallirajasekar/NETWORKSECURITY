from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.expection.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig

from NetworkSecurity.components.model_trainer import ModelTrainer
from NetworkSecurity.entity.config_entity import ModelTrainerConfig

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
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data validation Completed")
        print(data_validation_artifact)
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info('Data Transformation Started')
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transfromation()
        print(data_transformation_artifact)
        logging.info("Data Transformation Completed")


        logging.info("Model training has started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("Model Training Artifacts created")




        

    except Exception as e:
        raise NetworkSecurityException(e,sys)

