import os 
import sys

from NetworkSecurity.expection.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier

from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from NetworkSecurity.entity.config_entity import ModelTrainerConfig

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

from NetworkSecurity.utils.main_utils.utils import save_object,load_object
from NetworkSecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
from NetworkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def train_model(self,X_train,y_train,x_test,y_test):
        models={
            "Random Forest":RandomForestClassifier(verbose=1),
            "Decision Tree":DecisionTreeClassifier(),
            "Gardient Boosting":GradientBoostingClassifier(verbose=1),
            "Logistic regression":LogisticRegression(verbose=1),
            "AdaBoost":AdaBoostClassifier()
        }

        params={
            "Decision Tree":{
                'criterion':['gini','entropy','log_loss'],

            },
            "Random Forest":{
                'n_estimators':[8,16,32,128,256]

            },

            "Gradient Boosting":{
                'learning_rate':[.1,0.01]
            },
           
            "Logistic Regression":{},
            "AdaBoost":{
                'n_estimators':[8,16]
            }

        }

        model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=x_test,y_test=y_test,models=models,params=params)

        best_model_score=max(sorted(model_report.values()))

        ## To get the Best Model from the Dictionary

        best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]

        best_model=models[best_model_name]
        y_train_pred=best_model.predict(X_train)

        classification_train_metric=get_classification_score(y_true=y_test,y_pred=y_train_pred)

        y_test_pred=best_model.predict(x_test)

        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)

        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)

        save_object("final_model/model.pkl",best_model)

        ## Model Trained Artifact

        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,train_metric_artifact=classification_train_metric,test_metric_artifact=classification_test_metric)

        logging.info(f"Model Trainer Artifact:{model_trainer_artifact}")

        return model_trainer_artifact
    

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            #Loading training and Testing array 
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test=(train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1])

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)