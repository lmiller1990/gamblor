import pandas as pd

def team_games(df, team):
    return df[
                ( df['team'] == team ) & 
                ( df['player'] == 'Team' )
            ].drop_duplicates(subset=['gameid'])

def load_data(path, csv):
    df = pd.read_csv("data.csv")
    odds = pd.read_csv(path + "/" + csv)
    return df, odds

