import os
import sys
from src.logger import logging
from src.exception import Customexception

import pandas as pd

from src.utils import load_object

class PredictData:
    def __init__(self) :
        pass
    def predict(self,features):

        try:
            print("inside it")
          
             
            model_path = 'src/components/artifacts/model.pkl'
            preprocessor_path = 'src/components/artifacts/preprocessor.pkl'
            
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            
            print(features)
            data_scaled=preprocessor.transform(features)
            print(data_scaled)
            pred=model.predict(data_scaled)

            print(pred)

            return pred
        except Exception as e:
            raise Customexception(e,sys)




class Matchstat:
    def __init__(self,  battingteam: str, bowlingteam: str,currentscore: str,remainingovers:str,remainingwickets:str,runrate:str, requiredrunrate:str):
        self.battingteam = battingteam
        self.bowlingteam = bowlingteam
        self.currentscore = currentscore
        self.remainingovers = remainingovers
        self.remainingwickets = remainingwickets
        self.runrate = runrate
        self.requiredrunrate = requiredrunrate
        
        
        
        

    def get_data_as_dataframe(self):
        try:
            Matchstat_dict={
            "batting_team": [self.battingteam],
            "bowling_team": [self.bowlingteam],
            "current_score": [self.currentscore],
            "remaining_overs": [self.remainingovers],
            "remaining_wickets":[self.remainingwickets],
            "run_rate":[self.runrate],
            "required_run_rate":[self.requiredrunrate] 
        
                 }
            print("the dict is ",Matchstat_dict)
            return pd.DataFrame(Matchstat_dict)

        except Exception as e:
            raise Customexception (e,sys)
