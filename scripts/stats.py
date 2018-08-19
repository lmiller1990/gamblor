import pandas as pd
import numpy as np

def average_kills_and_deaths(df, league):
    """
    Returns average kills and deaths by league.

    Arguments:

    df: the dataframe containing the data.
    league: the league you are interested in. Eg: 'NALCS'
    
    Returns: An array containing [average_kills, average deaths]
    """
    all_games = df[df['league'] == league].drop_duplicates(subset=['gameid', 'team'])
    return [ 
                all_games[['teamkills']].mean()[0], 
                all_games[['teamdeaths']].mean()[0] 
            ]

def median_kills_and_deaths(df, league):
    """
    Returns median kills and deaths by league.

    Arguments:

    df: the dataframe containing the data.
    league: the league you are interested in. Eg: 'NALCS'
    
    Returns: An array containing [median_kills, median_deaths]
    """

    all_games = df[df['league'] == league].drop_duplicates(subset=['gameid', 'team'])
    return [ np.ma.median(all_games[['teamkills']]), np.ma.median(all_games[['teamdeaths']]) ]

def team_medians_kill_and_team(df, team):
    """
    Returns median kills and deaths by team.

    Arguments:

    df: the dataframe containing the data.
    team: the team you are interested in. Eg: 'Echo Fox'
    
    Returns: An array containing [median_kills, median_deaths]
    """

    games = df[
                ( df['team'] == team ) & 
                ( df['player'] == 'Team' )
            ].drop_duplicates(subset=['gameid'])

    return [ 
                np.ma.median(games[['teamkills']]), 
                np.ma.median(games[['teamdeaths']]) 
            ]


def team_average_kill_and_death(df, team):
    """
    Returns average kills and deaths by team.

    Arguments:

    df: the dataframe containing the data.
    team: the team you are interested in. Eg: 'Echo Fox'
    
    Returns: An array containing [average_kills, average_deaths]
    """

    games = df[
                ( df['team'] == team ) & 
                ( df['player'] == 'Team' )
            ].drop_duplicates(subset=['gameid'])

    return [ 
                games[['teamkills']].mean()[0], 
                games[['teamdeaths']].mean()[0] 
            ]

