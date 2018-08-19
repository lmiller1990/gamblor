import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
import data_utils
from collections import OrderedDict
import numpy as np
from data_utils import load_and_clean_data, team_games, teams_by_league, games_by_league

df = load_and_clean_data()

corr = {}
games = games_by_league(df, 'nalcs')
teams = teams_by_league(df, 'nalcs')

# Corr
#for team in teams:
#    games = team_games(df, team).dropna()
#    corr[team] = games[['result', 'fbaron']].corr()
#
#for k, v in corr.items():
#    print(k)
#    print(v)
#    print("\n")
#
#
#print("\n")
#print("\n")
#print(df['result fbaron'.split()].corr())
#print(OrderedDict(sorted(corr.items(), key=itemgetter(1), reverse=True)))

teams = [['cloud9', 'flyquest'], ['counter logic gaming', 'golden guardians'], ['optic gaming', '100 thieves'], ['echo fox', 'clutch gaming'], ['team solomid', 'team liquid']]

losses = games[games.result == 0]
wins = games[games.result == 1]

for team in teams[4]:
    print("\nteam", team)
    print("Winning stats")
    print("Tower kills median", np.ma.median(wins[wins.team == team].teamkills))

    print("\nLosing stats")
    print("Tower kills median", np.ma.median(losses[losses.team == team].teamkills))


