import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
import data_utils
from collections import OrderedDict
from data_utils import load_and_clean_data, team_games, teams_by_league

df = load_and_clean_data()

corr = {}
teams = teams_by_league(df, 'lck')

for team in teams:
    games = team_games(df, team).dropna()
    corr[team] = games[['result', 'fbaron']].corr()

for k, v in corr.items():
    print(k)
    print(v)
    print("\n")


print("\n")
print("\n")
print(df['result fbaron'.split()].corr())


#print(OrderedDict(sorted(corr.items(), key=itemgetter(1), reverse=True)))
