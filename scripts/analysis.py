import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
import data_utils
from collections import OrderedDict
import numpy as np
from data_utils import load_and_clean_data, team_games, teams_by_league, games_by_league, opponent_games
#from sklearn.cross_validation import train_test_split
#from sklearn.linear_model import LinearRegression
from graphs import running_first_stat

df = load_and_clean_data()

def history(team):
    games = team_games(df, team)
    opponents = opponent_games(df, team, games.gameid)

    result = games.merge(opponents, on="gameid")[['date', 'side', 'team', 'opponent', 'fb', 'fbtime', 'ft', 'fttime', 'fd', 'result']] 

    print(result.round(2))

team_market = 'tower'
approx_total = 13.5

league_teams = ['sk telecom t1', 'afreeca freecs'] # , 'sk telecom t1', 'kingzone dragonx', 'afreeca freecs']#teams_by_league(df, ['lck']).tolist()

fields = ['team', 'opponent', 'team' + team_market + 'kills', 'opp' + team_market + 'kills', team_market + 'kills', 'above']

team = 'sk telecom t1'
league_teams.remove(team)
top_teams = league_teams # ['gen.g' ] #, 'kingzone dragonx', 'sk telecom t1',] # 'afreeca freecs', 'hanwha life esports']

games = team_games(df, team)
opponents = opponent_games(df, team, games.gameid)
games = games.merge(opponents, on="gameid")

games = games[games['opponent'].isin(top_teams)]
games[team_market + 'kills'] = games['team' + team_market + 'kills'] + games['opp' + team_market + 'kills']
games['above'] = (games['team' + team_market + 'kills'] + games['opp' + team_market + 'kills'] > 12.5)

games[fields].reset_index().to_csv("turrets.csv")
print(games[fields])
print('Games above 12.5 ' + team_market, games[games.above == True].shape)
print('Games below 12.5 ' + team_market, games[games.above == False].shape)

all_av_towers = []
for the_team in top_teams + [team]:
    av_towers = games[(games.team == the_team) | (games.opponent == the_team)][team_market + 'kills'].mean()
    all_av_towers.append(av_towers)
    print(the_team, av_towers)

fig = plt.figure()
ax = fig.add_subplot(111)

short_names = list(map(lambda x: x[:8], top_teams + [team]))

plt.bar(short_names, all_av_towers)

ax.set_yticks(np.arange(0,approx_total))
ax.yaxis.grid()
plt.xticks(rotation=approx_total)

totals = []
for i in ax.patches:
    totals.append(i.get_height())

# set individual bar lables using above list
total = sum(totals)

# set individual bar lables using above list
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()-.03, i.get_height()+.5, \
            str(round(i.get_height(), 2)), fontsize=8,
                color='dimgrey')

ax.tick_params(labelsize='small')

plt.ylim([0, approx_total])
plt.show()

print(df.columns)
#team = 'clutch gaming'
#team_games = team_games(df, team)
#
#f_only = ['week', 'team', 'fbaron', 'opponent', 'result']
#
#print(result)
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
