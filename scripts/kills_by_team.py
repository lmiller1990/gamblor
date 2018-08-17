import pandas as pd
from operator import itemgetter
from collections import OrderedDict
import numpy as np
from constants import teams_by_league
from stats import average_kills_and_deaths, team_average_kill_and_death
from data_utils import team_games

THRESHOLD = 22.5

df = pd.read_csv("data.csv")
df['team'] = df['team'].str.lower()
matches = [
    ['team liquid', 'echo fox'],
    ['100 thieves', 'cloud9'],
    ['counter logic gaming', 'clutch gaming'],
    ['golden guardians', 'flyquest'],
    ['optic gaming', 'team solomid']
]

def flatten(arr):
    return [item for sublist in arr for item in sublist] 

def kd_above_below_threshold(df, team, threshold):
    matches = team_games(df, team=team)
    matches['kd'] = matches['teamkills'] + matches['teamdeaths']
    matches['above_threshold'] = matches[['kd']] > threshold 
    above = matches[matches['above_threshold'] == True].shape[0]
    below = matches[matches['above_threshold'] == False].shape[0]
    return [above, below]

all_teams = flatten(matches)
all_kd = {}
for team in all_teams:
    [av_kill, av_death] = team_average_kill_and_death(df, team)
    all_kd[team] = av_kill + av_death


print(OrderedDict(sorted(all_kd.items(), key=itemgetter(1), reverse=True)))

[league_average_kills ,_] = average_kills_and_deaths(df,league='NALCS')

for [t0, t1] in matches:
    [t0_above, t0_below] = kd_above_below_threshold(df, t0, THRESHOLD)
    [t1_above, t1_below] = kd_above_below_threshold(df, t1, THRESHOLD)
    print(t0, t0_above / (t0_above + t0_below))
    print(t1, t1_above / (t1_above + t1_below))
