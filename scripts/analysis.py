import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
import data_utils
from collections import OrderedDict
import numpy as np
from data_utils import load_and_clean_data, team_games, teams_by_league, games_by_league, opponent_games
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression

fields = 'team player teamkills teamdeaths'.split()
df = load_and_clean_data()
#opponents = opponent_games(df, 'team solomid', team_games.gameid)

#result = games.merge(opponents, on="gameid")[['week', 'game', 'team', 'opponent', 'side', 'result', 'teamkills', 'teamdeaths']]

fields = ['fb', 'ft', 'fd', 'fbaron']

print(df.league.unique())
teams = teams_by_league(df, ['nalcs'])
stats = {}

for f in fields:
    stats[f] = []
    for team in teams:
        games = team_games(df, team)
        games.replace(" ", np.nan, inplace=True)
        taken = games[f].sum()
        total = games[f].shape[0]
        stats[f].append(taken/total)

stats['wins'] = []
for team in teams:
    stats['wins'].append(team_games(df, team).result.sum())

result = pd.DataFrame(stats, index=teams)
#print(result.sort_values(by='wins', ascending=False))
#(['gameid', 'url', 'league', 'split', 'date', 'week', 'game', 'patchno',
#       'playerid', 'side', 'position', 'player', 'team', 'champion', 'ban1',
#       'ban2', 'ban3', 'ban4', 'ban5', 'gamelength', 'result', 'k', 'd', 'a',
#       'teamkills', 'teamdeaths', 'doubles', 'triples', 'quadras', 'pentas',
#       'fb', 'fbassist', 'fbvictim', 'fbtime', 'kpm', 'okpm', 'ckpm', 'fd',
#       'fdtime', 'teamdragkills', 'oppdragkills', 'elementals',
#       'oppelementals', 'firedrakes', 'waterdrakes', 'earthdrakes',
#       'airdrakes', 'elders', 'oppelders', 'herald', 'heraldtime', 'ft',
#       'fttime', 'firstmidouter', 'firsttothreetowers', 'teamtowerkills',
#       'opptowerkills', 'fbaron', 'fbarontime', 'teambaronkills',
#       'oppbaronkills', 'dmgtochamps', 'dmgtochampsperminute', 'dmgshare',
#       'earnedgoldshare', 'wards', 'wpm', 'wardshare', 'wardkills', 'wcpm',
#       'visionwards', 'visionwardbuys', 'visiblewardclearrate',
#       'invisiblewardclearrate', 'totalgold', 'earnedgpm', 'goldspent', 'gspd',
#       'minionkills', 'monsterkills', 'monsterkillsownjungle',
#       'monsterkillsenemyjungle', 'cspm', 'goldat10', 'oppgoldat10', 'gdat10',
#       'goldat15', 'oppgoldat15', 'gdat15', 'xpat10', 'oppxpat10', 'xpdat10',
#       'csat10', 'oppcsat10', 'csdat10', 'csat15', 'oppcsat15', 'csdat15'],
#df = load_and_clean_data()
#corr = {}
#
#fields = 'result side fb fd ft fbaron'.split()
#
#def do_corr(team):
#    games = games_by_league(df, [team])[fields]
#    games.replace(' ', np.nan, inplace=True)
#    games.dropna(inplace=True)
#    X = games['side fb fd ft fbaron'.split()]
#    y = games[['result']]
#    teams = teams_by_league(df, [team])
#
#    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
#
#    lm = LinearRegression()
#    lm.fit(x_train, y_train)
#
#    cdf=pd.DataFrame(lm.coef_[0], X.columns, columns=['Coeff'])
#    print("Blue: 0, Red: 1")
#    print("total games", X.shape)
#    print(team)
#    print(cdf.round(2))
#
#do_corr('nalcs')
#do_corr('lck')
#do_corr('eulcs')
