import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from NetworkSecurity.constants.training_pipeline import TARGET_COLUMN
from NetworkSecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from NetworkSecurity.entity.artifact_entity import (
    DataTransformationArtifact,DataValidationArtifact
)

from NetworkSecurity.entity.config_entity import DataTransformationConfig
from NetworkSecurity.expection.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.utils.main_utils.utils import save_numpy_array,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_tranformer_object(cls)->Pipeline:
        """
        It initiates the KNN imputer with Parmater Specified in the training Pipeline.py file
        and returns the Pipeline object with the KNNImputer object as the first step
        
        Args:

           cls:DataTransformation"

        Return:
            A pipeline Object
        """

        logging.info(
            "Enter get_data_transformer_object method of Transformation class"
        )
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Intialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        

    def initiate_data_transfromation(self)->DataTransformationArtifact:
        logging.info('Entered initiate_data_method of Data Transformation Class')
        try:
            logging.info('Start data Transformation')
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ##training dataframe

            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            ##testing dataframe

            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            preprocessor=self.get_data_tranformer_object()

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transform_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transform_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            train_arr=np.c_[transform_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transform_input_test_feature,np.array(target_feature_test_df)]

            #Save Numpy array Data

            save_numpy_array(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)

            save_object("final_model/preprocessor.pkl",preprocessor_object)

            ## Preparing Artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)




