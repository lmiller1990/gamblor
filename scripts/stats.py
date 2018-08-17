import pandas as pd
import numpy as np

def average_kills_and_deaths(df, league):
    all_games = df[df['league'] == league].drop_duplicates(subset=['gameid', 'team'])
    return [ 
                all_games[['teamkills']].mean()[0], 
                all_games[['teamdeaths']].mean()[0] 
            ]

def median_kills_and_deaths(df, league):
    all_games = df[df['league'] == league].drop_duplicates(subset=['gameid', 'team'])
    return [ np.ma.median(all_games[['teamkills']]), np.ma.median(all_games[['teamdeaths']]) ]

def team_medians_kill_and_team(df, team):
    games = df[
                ( df['team'] == team ) & 
                ( df['player'] == 'Team' )
            ].drop_duplicates(subset=['gameid'])

    return [ 
                np.ma.median(games[['teamkills']]), 
                np.ma.median(games[['teamdeaths']]) 
            ]


def team_average_kill_and_death(df, team):
    games = df[
                ( df['team'] == team ) & 
                ( df['player'] == 'Team' )
            ].drop_duplicates(subset=['gameid'])

    return [ 
                games[['teamkills']].mean()[0], 
                games[['teamdeaths']].mean()[0] 
            ]

