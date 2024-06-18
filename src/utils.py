import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin
import os
import dill
import sys
from src.exception import Customexception
from src.logger import logging
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix

def save_obj(file_path,obj):

    try:
        dir_path=os.path.dirname(file_path)
        logging.info('Encoding model is saving')
        

        os.makedirs(dir_path,exist_ok=True)

        


        with open(file_path, 'wb') as file:
            dill.dump(obj, file)
        logging.info('Encoding model saved')

    except Exception as e:
       raise Customexception(e,sys)


# Define the function to calculate remaining overs
def calculate_remaining_overs(row, previous_over, previous_remaining_overs,previous_ball_extra):
    if row['over'] != previous_over:
        previous_ball_extra = 0
    
    if pd.notnull(row['extras_type']):
        ball = 0
        if row['extras_type'] in ['wides', 'noball'] or (row['extras_type'] in ['wides', 'bye', 'penalty'] and row['extra_runs'] == 5):
            previous_ball_extra = 1
            return previous_remaining_overs, previous_ball_extra  # Return previous remaining overs
        if  row['extras_type'] in ['legbyes', 'byes'] and row['extra_runs'] < 5:
            ball = row['ball']
    else:
        ball = row['ball']
    
    if previous_ball_extra == 1:
        ball -= 1

    remaining_overs = 19.6 - row['over'] - (ball) / 10
    # Retain only one decimal place
    remaining_overs = float(f"{remaining_overs:.1f}")
    return remaining_overs, previous_ball_extra


def data_preparation(deliveries,matches):

    deliveries['current_score'] = deliveries.groupby(['inning', 'match_id'])['total_runs'].cumsum()

    deliveries['remaining_wickets'] = 10 - deliveries.groupby(['inning', 'match_id'])['is_wicket'].cumsum()


    previous_over = None
    previous_remaining_overs = 20.0



    # Loop through each row to calculate the remaining overs
    remaining_overs_list = []
    previous_ball_extra = 0

    for index, row in deliveries.iterrows():
        remaining_overs, previous_ball_extra = calculate_remaining_overs(row, previous_over, previous_remaining_overs,previous_ball_extra)
        remaining_overs_list.append(remaining_overs)
        previous_remaining_overs = remaining_overs
        previous_over = row['over']

    # Add the calculated remaining overs to the DataFrame
    deliveries['remaining_overs'] = remaining_overs_list
    first_innings_total = deliveries[deliveries['inning'] == 1].groupby('match_id')['total_runs'].sum().reset_index()
    first_innings_total.rename(columns={'total_runs': 'targetscore'}, inplace=True)


    # Merge the target score into the original DataFrame
    deliveries = deliveries.merge(first_innings_total, on='match_id', how='left')
    new_df=deliveries[deliveries['inning']==2]
    new_df['run_rate'] = new_df['current_score'] / (new_df['over'] + new_df['ball'] / 10)


    new_df['required_run_rate'] = (new_df['targetscore'] - new_df['current_score']) / new_df['remaining_overs']
    columns_to_retain = ['match_id', 'inning', 'batting_team', 'bowling_team','current_score', 'remaining_wickets', 'remaining_overs', 'run_rate', 'required_run_rate']

# Drop all other columns
    modified = new_df[columns_to_retain]
    matches_filtered = matches[['id', 'winner']]
    matches_filtered.rename(columns={'id': 'match_id'}, inplace=True)
    modified = modified.merge(matches_filtered, on='match_id', how='left')
    modified.drop(columns=['match_id','inning'],inplace=True,axis=1)
    teams_to_drop = ['Kochi Tuskers Kerala', 'Rising Pune Supergiants', 'Gujarat Lions', 'Pune Warriors India','Rising Pune Supergiant','Pune Warriors']

# Dropping rows where 'batting_team' or 'bowling_team' is in teams_to_drop
    modified = modified[~modified['batting_team'].isin(teams_to_drop) & ~modified['bowling_team'].isin(teams_to_drop)]
    team_replacements = {
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Royal Challengers Bengaluru': 'Royal Challengers Bangalore',
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings'
}

# Apply replacements to all columns in the dataframe
    modified = modified.apply(lambda col: col.replace(team_replacements) if col.name in ['batting_team', 'bowling_team', 'winner'] else col)
    modified['required_run_rate'] = modified['required_run_rate'].replace([np.inf, -np.inf], 0)
    return modified


class CustomLabelencoder(BaseEstimator, TransformerMixin):
    def __init__(self, categorical_columns):
        self.categorical_columns = categorical_columns
        self.encoders = {col: LabelEncoder() for col in categorical_columns}

    def fit(self, X, y=None):
        for col in self.categorical_columns:
            self.encoders[col].fit(X[col])
        return self

    def transform(self, X):
        X_transformed = X.copy()
        for col in self.categorical_columns:
            X_transformed[col] = self.encoders[col].transform(X[col])
        X_transformed_array = X_transformed[self.categorical_columns].values
        
        # Extract the non-categorical columns and convert to array
        non_cat_columns = X.drop(columns=self.categorical_columns).values
        
        # Concatenate the non-categorical columns with the encoded columns
        arr = np.concatenate([non_cat_columns, X_transformed_array], axis=1)
        
       
        return arr

def evaluvate_model(X_train,X_test,y_train,y_test,model):
    try:
            report={}
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            # make predictions
            y_test_pred = model.predict(X_test)
            # Calculate the accuracy of the model

            accuracy_train = accuracy_score(y_train, y_train_pred)
            
            accuracy_test= accuracy_score(y_test, y_test_pred)
            conf_matrix_train= confusion_matrix(y_train, y_train_pred)
            conf_matrix_test= confusion_matrix(y_test, y_test_pred)
            class_report=classification_report(y_test, y_test_pred)


            print("Class_report is:",class_report)
            print("ConfusionMatrix is:",conf_matrix_test)
            report[model]=accuracy_test
            return report
            
    except Exception as e:

            raise Customexception(e,sys)
    

def load_object(file_path):
    try:
        with open(file_path, 'rb') as file:
                return dill.load(file)
            
    except Exception as e:
        raise Customexception(e,sys)