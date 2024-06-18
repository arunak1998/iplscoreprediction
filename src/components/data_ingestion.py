from src.exception import Customexception
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import sys
from src.utils import data_preparation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from dataclasses import dataclass


@dataclass
class DataingestionConfig:
    train_data_path=os.path.join("artifacts","train.csv")
    test_data_path=os.path.join("artifacts","test.csv")
    raw_data_path=os.path.join("artifacts","raw_data.csv")

class DataIngestion:
    def __init__(self) :

        self.ingestion_config=DataingestionConfig()


    def initiate_data_ingestion(self):

        logging.info("Entering Data Ingestion method")


        try:
            current_dir = os.path.dirname(__file__)

            # Construct the relative path to the CSV file
            csv_path = os.path.join(current_dir, '..', '..', 'notebook', 'deliveries.csv')
            csv_path1 = os.path.join(current_dir, '..', '..', 'notebook', 'matches.csv')
            de=pd.read_csv(csv_path)
            matches=pd.read_csv(csv_path1)
           
            logging.info("Data Preparation Started")


            modified_df=data_preparation(de,matches)
            logging.info("Data Preparation completed")
            logging.info("Train data test data split Initiated")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)


            modified_df.to_csv(self.ingestion_config.raw_data_path,header=True,index=False)

            train_set,test_set=train_test_split(modified_df,random_state=42,test_size=0.2)
            train_set.to_csv(self.ingestion_config.train_data_path,header=True,index=False)
            test_set.to_csv(self.ingestion_config.test_data_path,header=True,index=False)


            logging.info("Train data test data split completed")

            logging.info("Data Ingestion Completed")

            return (
               self.ingestion_config.train_data_path,
               self.ingestion_config.test_data_path
            )


        except Exception as e:

            raise Customexception(e,sys)
        

if __name__=="__main__":

    obj=DataIngestion()
    train_path,test_path=obj.initiate_data_ingestion()
    obj1=DataTransformation()
    train_arr,test_arr=obj1.initiate_data_transformation(train_path,test_path)
    obj3=ModelTrainer()
    obj3.initiate_model_trainer(train_arr,test_arr)




