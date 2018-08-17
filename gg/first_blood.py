import sys
import pandas as pd

fields = 'gameid week game team fb fbtime'.split()
df = pd.read_csv("data.csv")
#odds = pd.read_csv("guides/fb_odds.csv")
odds = pd.read_csv("guides/fd_odds_beteasy.csv")

def get_fb_chance(team):
    data = df[(df['team'] == team) & (df['player'] == 'Team')]
    got_fb = data[data['fb'] == '1']

    return (got_fb.shape[0] / data.shape[0]) * 100

def fetch_odds(teams):
    t1, t2 = list(teams.keys())
    match = odds[( odds['team_1'] == t1 ) & ( odds['team_2'] == t2 )]

    t1_odds = match['team_1_odds'].iloc[0]
    t2_odds = match['team_2_odds'].iloc[0]

    print(t1, " vs ", t2)
    print("-----------------------------------")
    print("EV for ", t1, teams[t1] * t1_odds)
    print("EV for ", t2, teams[t2] * t2_odds)
    print("\n\n=================================\n\n")

teams = []
for i in range(odds.shape[0]):
    teams = [ odds.iloc[i]['team_1'], odds.iloc[i]['team_2'] ]

    fb_chances = {}
    for team in teams:
        fb_percent = get_fb_chance(team)
        fb_chances[team] = fb_percent

    team_0 = teams[0]
    team_1 = teams[1]

    fb_odds = {}
    fb_odds[team_0] = (fb_chances[team_0] + (100 - fb_chances[team_1])) / 200
    fb_odds[team_1] = (fb_chances[team_1] + (100 - fb_chances[team_0])) / 200

    fetch_odds(fb_odds)
