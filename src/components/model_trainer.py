import pandas as pd
import numpy as np
import os 
import sys
from dataclasses import dataclass
from src.exception import Customexception
from src.logger import logging
from xgboost import XGBClassifier

from src.utils import save_obj,evaluvate_model
from sklearn.metrics import accuracy_score


@dataclass
class ModelTrainerConfig:
    preprocessor_obj_file=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self) :
        self.model_train_config=ModelTrainerConfig()

    
    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging .info("Splliting Traning and Test data ")

            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1]
            )
          

            modelXG = XGBClassifier(
            colsample_bytree=1.0,
            gamma=0,
            reg_lambda=1,  # 'lambda' parameter is referred to as 'reg_lambda' in the XGBClassifier
            learning_rate=0.2,
            max_depth=5,
            n_estimators=200,
            subsample=0.8,
            objective='binary:logistic',
            eval_metric='logloss',
            use_label_encoder=False
)
            model_report:dict=evaluvate_model(X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,model=modelXG)

            value_list = list(model_report.values())
            model_score=value_list[0]
            print(model_score)

            if model_score<0.8:
                raise Customexception("This is not best model")
            logging.info("This is best model for this ")


            save_obj(
                file_path=self.model_train_config.preprocessor_obj_file,
                obj=modelXG
            )

            predicted=modelXG.predict(X_test)

            accuracy=accuracy_score(y_test,predicted)

            return accuracy
        
        except Exception as e:
            raise Customexception(e,sys)
