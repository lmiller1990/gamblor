import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
import data_utils
from collections import OrderedDict
import numpy as np
from data_utils import load_and_clean_data, team_games, teams_by_league, games_by_league, opponent_games
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression

team = '100 thieves'
df = load_and_clean_data()

games = df[(df.league == 'nalcs') & (df.ft == 1.0) & (df.player != 'Team')][['gameid', 'player', 'ft', 'team', 'result']]

print(games)

team_games = team_games(df, team)
opponents = opponent_games(df, team, team_games.gameid)

result = team_games.merge(opponents, on="gameid")[['week', 'game', 'team', 'opponent', 'side', 'result', 'fd']]
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
