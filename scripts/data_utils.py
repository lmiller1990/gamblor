import pandas as pd
import numpy as np

def games_only(df):
    return df.drop_duplicates(subset=['gameid', 'team'])

def games_by_league(df, league):
    return df[df.league.isin(league)].drop_duplicates(subset=['gameid', 'team'])

def teams_by_league(df, league=["nalcs"]):
    data = df[df.league.isin(league)].drop_duplicates(subset=['team'])['team']
    return data.values

def get_opponents(df):
    """
    gets opponents for a df of games
    """
    opponents = []
    games = games_only(df)
    for idx, row in df.iterrows():
        print(idx)
        op = games[(games.gameid == row.gameid) & (games.team != row.team)].team.values[0]
        opponents.append(op)

    return opponents

def team_games(df, team):
    """
    Returns all unique games played by a team.

    Arguments:

    df: the dataframe containing the data.
    team: the team you are interested in. Eg: "Echo Fox"
    """
    print(df[
        ( df['team'] == team ) & 
        ( df['player'] == 'Team' )
        ].drop_duplicates(subset=['gameid']).shape)
    return df[
                ( df['team'] == team ) & 
                ( df['player'] == 'Team' )
            ].drop_duplicates(subset=['gameid'])

def load_data(path, csv):
    return pd.read_csv(path + "/" + csv)

def load_and_clean_data(data='data.csv', league=None):
    df = pd.read_csv(data)
    df.team = df.team.str.lower()
    df.league = df.league.str.lower()

    if league:
        df = df[df.league == league]

    df.dropna(subset=['gameid'], inplace=True)
    df['opponent'] = get_opponents(df)

    print(df)
    return df.replace({ "1": 1.0, "0": 0.0, 1: 1.0, 0: 0.0, 'Blue': 0.0, 'Red': 1.0 })

def opponent_games(df, team, gameids):
    """
    Returns opponents for a given team.

    Arguments:

    df: the dataframe containing the data.
    team: the team you are interested in.
    games: a array of gameids the team played in.
    """
    games = df[df.gameid.isin(gameids)]
    opponent_games = games[games.team != team].drop_duplicates(subset=['gameid'])[['gameid', 'team']]
    opponent_games.columns = ['gameid', 'opponent']

    return opponent_games

def history(df, team, opponent):
    """ 
    Returns game history for a team

    Arguments:

    df: the dataframe
    team: team you are interested in
    """
    if opponent:
        games = df[(df.team == team) & (df.opponent == opponent)]#team_games(df, team)
    else:
        games = df[df.team == team]#team_games(df, team)

    result = games[['team', 'opponent', 'player', 'champion', 'fb', 'ft', 'result']]

    return result.round(2)

