import pandas as pd
from scripts.data_utils import load_and_clean_data, games_only

df = load_and_clean_data()
print(df.columns)

df.to_csv("data_with_opponent.csv")

#print(df[['gameid', 'team', 'opponent']])

#BLUE = 0.
#RED = 1.
#
#fields = 'gameid team player teamkills teamdeaths fb fd ft fbaron result teamkills teamdeaths teamdragkills oppdragkills teambaronkills oppbaronkills teamtowerkills opptowerkills'.split()
#
#
#rows = []
##rows.append('red_team,blue_team,fb_team,fd_team,ft_team,fbaron_team)
#
#def to_s(series):
#    return series.iloc[0]
#
#games = df[( df.league == 'lck' ) & ( df.player == 'Team' ) ]
#unique_games = games.drop_duplicates(subset=['gameid'])
#opponents = [] # pd.Series
#
#def get_opponent(games_by_teams_df, gameid, team):
#    oppo = games_by_teams_df[ (games_by_teams_df.gameid == gameid) & (games_by_teams_df.team != team) ]['team']
#    return oppo.iloc[0]
#
#    
##for index, row in unique_games.iterrows():
##    print('--------\n')
##    print(row.gameid, row.team, row.side)
##    oppo = games[ (games.gameid == row.gameid) & (games.team != row.team) ]
##    print(to_s(oppo.gameid), to_s(oppo['team']), to_s(oppo['side']))
##    print(get_opponent(games, row.gameid, row.team))
##    #opponents.append(to_s(oppo['team']))
##    #print(row.gameid, row['team'])
##
##    #opponent = games[ (by_team.gameid == row.gameid) & (by_team.team != row.team) ]
##    #print(opponent.gameid, opponent.team)
##    #print('opponent', opponent['player'])
##
#print(games.shape)
#print(len(opponents)) 
