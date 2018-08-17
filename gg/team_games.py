import sys
import pandas as pd

team = sys.argv[1]
df = pd.read_csv("data.csv")

fields = 'gameid week game team side gamelength result teamkills teamdeaths'.split()
team_games = df[df['team'] == team].drop_duplicates(subset=['gameid'])[fields]
team_game_ids = team_games['gameid']

games = df.loc[df['gameid'].isin(team_game_ids)]
# unique_fields = ['week','game','team','gameid']
unique_fields = ['gameid']
opponents = games[games['team'] != team].drop_duplicates(subset=unique_fields)[['gameid', 'team']]
opponents.columns = ['gameid', 'opponent']

result = pd.merge(team_games, opponents, on='gameid')

result.insert(5, 'the_opponent', result['opponent'])
result.drop('opponent', axis=1, inplace=True)
print(result)
