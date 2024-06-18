import sys
import os
from dataclasses import dataclass
from src.utils import save_obj
from src.utils import CustomLabelencoder
import numpy as np

import pandas as pd

from sklearn.pipeline import Pipeline
from src.logger import logging
from src.exception import Customexception


@dataclass
class DataTransformerConfig:
    preprocessor_obj_file=os.path.join("artifacts","preprocessor.pkl")
    


class DataTransformation:
    def __init__(self) :
        self.data_transformation_config=DataTransformerConfig()

    def get_data_transformer_object(self):
        '''
        This Function is Responsible for Data Transformation
        '''
        try:
            categorical_features=['batting_team','bowling_team']
             
           
            
            
           
            logging.info('Categorical_features Encoding is Completed')
           
            


            preprocessor = Pipeline([
             ('custom_encoder', CustomLabelencoder(categorical_columns=categorical_features)),
    
                     ])
           
           
            return preprocessor
    
        except Exception as e:
            raise Customexception(e,sys)
        


    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_data=pd.read_csv(train_path)
            test_data=pd.read_csv(test_path)

            train_data['winner_encode'] = train_data.apply(lambda row: 1 if row['winner'] == row['batting_team'] else 0, axis=1)
            test_data['winner_encode'] = test_data.apply(lambda row: 1 if row['winner'] == row['batting_team'] else 0, axis=1)
            train_data.drop(columns=['winner'],inplace=True,axis=1)
            test_data.drop(columns=['winner'],inplace=True,axis=1)
          

            logging.info('Read Train and test data Completed')

            logging.info('Obtaining PrepProcesing Object')


            

            preprocessing_object=self.get_data_transformer_object()

            target_column="winner_encode"
           
         
            

           
           
            input_training_feature=train_data.drop(columns=['winner_encode'],axis=1)
           
            target_feature_train_df=train_data[target_column]

            input_test_feature=test_data.drop(columns=['winner_encode'],axis=1)
            target_feature_test_df=test_data[target_column]
            
          

           
          
            
            input_feature_train_arr=preprocessing_object.fit_transform(input_training_feature)
            input_feature_test_arr= preprocessing_object.transform(input_test_feature)
           
            logging.info("f lable ENcoding has been applied  Training and Test data ")

          
            
            

            train_arr=np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr=np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]
            print(test_arr.shape)
            logging.info('Preprocessing Completed')
           
            save_obj(
                file_path=self.data_transformation_config.preprocessor_obj_file,
                obj=preprocessing_object
            )

            return(
                train_arr,
                test_arr
            )
        

        except Exception as e:
            raise Customexception(e,sys)
        

    
