import pymongo
import pandas
import numpy as np

def insert():
    match = pandas.read_csv(r'D:\Projects\IplPrediction\iplwinnerprediction\notebook\matches.csv')
    team_replacements = {
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Royal Challengers Bengaluru': 'Royal Challengers Bangalore',
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings'
}

# Apply replacements to all columns in the dataframe
    match = match.apply(lambda col: col.replace(team_replacements) if col.name in ['team1', 'team2','winner'] else col)
    head_to_head_wins = {}

    # Iterate through each match
    for index, row in match.iterrows():
        team1 = row['team1']
        team2 = row['team2']
        winner = row['winner']
        
        # Ensure both teams are in the nested dictionaries
        if team1 not in head_to_head_wins:
            head_to_head_wins[team1] = {}
        if team2 not in head_to_head_wins:
            head_to_head_wins[team2] = {}
        if team2 not in head_to_head_wins[team1]:
            head_to_head_wins[team1][team2] = 0
        if team1 not in head_to_head_wins[team2]:
            head_to_head_wins[team2][team1] = 0

        # Increment head-to-head wins for the winner
        if winner == team1:
            head_to_head_wins[team1][team2] += 1
        elif winner == team2:
            head_to_head_wins[team2][team1] += 1

        # Add new columns for head-to-head wins in the match DataFrame
    match['bat_team_h2h_wins'] = 0
    match['bowl_team_h2h_wins'] = 0

    # Update the new columns with the head-to-head wins
    for index, row in match.iterrows():
        batting_team = row['team1']
        bowling_team = row['team2']
        
        if bowling_team in head_to_head_wins[batting_team]:
            match.at[index, 'bat_team_h2h_wins'] = head_to_head_wins[batting_team][bowling_team]
        if batting_team in head_to_head_wins[bowling_team]:
            match.at[index, 'bowl_team_h2h_wins'] = head_to_head_wins[bowling_team][batting_team]
    new_match = match[['team1', 'team2', 'bat_team_h2h_wins', 'bowl_team_h2h_wins']]
    new_match['sorted_teams'] = new_match.apply(lambda row: tuple(sorted([row['team1'], row['team2']])), axis=1)
    unique_combinations = new_match.drop_duplicates(subset=['sorted_teams']).drop(columns=['sorted_teams'])
    
    client = pymongo.MongoClient('mongodb+srv://aktooall:arun1998@cluster0.6m6bljh.mongodb.net/')

    my_db=client['Ml_project']
    match_summary = my_db.matchsummary
    for index, row in unique_combinations.iterrows():
        _id = np.random.randint(1000000000)
        row_dict = row.to_dict()
        row_dict['_id'] = _id
        match_summary.insert_one(row_dict)
    print('Inserted Sucessfullt') 
    team_name = 'Royal Challengers Bangalore'
    filtered_combinations = unique_combinations[(unique_combinations['team1'] == team_name) | (unique_combinations['team2'] == team_name)]
    print(filtered_combinations)
if __name__=='__main__':
    insert()