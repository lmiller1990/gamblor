import pandas as pd

def games_by_league(df, league="nalcs"):
    return df[df.league == league].drop_duplicates(subset=['gameid', 'team'])

def teams_by_league(df, league="nalcs"):
    return df[df.league == league].drop_duplicates(subset=['team'])['team'].values

def team_games(df, team):
    """
    Returns all unique games played by a team.

    Arguments:

    df: the dataframe containing the data.
    team: the team you are interested in. Eg: "Echo Fox"
    """
    return df[
                ( df['team'] == team ) & 
                ( df['player'] == 'Team' )
            ].drop_duplicates(subset=['gameid'])

def load_data(path, csv):
    df = pd.read_csv("data.csv")
    odds = pd.read_csv(path + "/" + csv)
    return df, odds

def load_and_clean_data():
    df = pd.read_csv("data.csv")

    df.team = df.team.str.lower()
    df.league = df.league.str.lower()
    return df.replace({ "1": 1.0, "0": 0.0, 1: 1.0, 0: 0.0 })
