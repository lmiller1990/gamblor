import pandas as pd
import argparse
from data_utils import load_and_clean_data
from common import get_first_chance_all_games
import numpy as np
from graphs import running_victories, running_first_stat, average_first_stat
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--teams", help="teams to include in analysis")
parser.add_argument("--exclude", help="teams to exlude from calcs", default='')
parser.add_argument("--league", help="league")
args = parser.parse_args()

df = load_and_clean_data(args.league)
exclude = args.exclude.split(',')
#df = df[~df.opponent.isin(exclude)]
#print(df[['team', 'result', 'opponent']])

html = ""

STATS = [
    { 'title': 'First Blood', 'name': 'fb' },
    { 'title': 'First Turret', 'name': 'ft' },
    { 'title': 'First Dragon', 'name': 'fd' },
    { 'title': 'First Baron', 'name': 'fbaron' }
]

def graph_for_stat_average(df, teams, stats):
    fig, ax = plt.subplots(nrows=2, ncols=2)
    i = 0
    for row in ax:
        for col in row:
            col.set_ylim([0, 100])
            for team in teams:
                col.set_title(stats[i] + "% (all-time av)")
                [total_games, chance] = average_first_stat(df, team, stats[i])

                col.plot(np.arange(1, total_games+1), np.array(chance) * 100, label=team)
            i = i + 1

    plt.legend()
    fig.tight_layout()
    fig.savefig('first.png')


for stat in STATS:
    odds_csv = pd.read_csv('odds/' + stat['name'] +  '/bet365.csv')
    team_one = None
    team_two = None

    for i in range(odds_csv.shape[0]):
        team_one = odds_csv.iloc[i]['team_1']
        team_two = odds_csv.iloc[i]['team_2']
        team_one_odds = odds_csv.iloc[i]['team_1_odds'] 
        team_two_odds = odds_csv.iloc[i]['team_2_odds']

        html += f"<h2>{stat['title']}</h2>"
        html += f"<h3>{team_one} ({team_one_odds}) vs {team_two} ({team_two_odds})</h3>"
        team_one_chance = get_first_chance_all_games(df, team_one, stat['name'], 1.)
        team_two_chance = get_first_chance_all_games(df, team_two, stat['name'], 1.)
        smallest = min(len(team_one_chance), len(team_two_chance))

        html += f"<table>"
        html += f"<tr>"
        html += f"<td>Games</td>"
        html += f"<td>{team_one}</td>"
        html += f"<td>{team_two}</td>"
        html += f"<td>T1 EV</td>"
        html += f"<td>T2 EV</td>"
        html += f"</tr>"

        for i in range(smallest):
            team_one_rel = (team_one_chance[i]['chance'] + (1 - team_two_chance[i]['chance'])) / 2
            team_two_rel = (team_two_chance[i]['chance'] + (1 - team_one_chance[i]['chance'])) / 2
            team_one_ev = round(team_one_rel * team_one_odds, 2)
            team_two_ev = round(team_two_rel * team_two_odds, 2)

            print(team_one, team_one_chance[i]['week_game']) 
            #print(team_two, team_two_chance[i+7]['week_game'])

            html += f"<tr>"
            html += f"<td>{team_one_chance[i]['week_game']} {team_two_chance[i]['week_game']}</td>"
            html += f"<td>{round(team_one_rel, 2)}</td>"
            html += f"<td>{round(team_two_rel, 2)}</td>"
            if team_one_ev > 1.1:
                html += f"<td><u>{team_one_ev}</u></td>"
            else:
                html += f"<td>{team_one_ev}</td>"

            if team_two_ev > 1.1:
                html += f"<td><u>{team_two_ev}</u></td>"
            else:
                html += f"<td>{team_two_ev}</td>"

            html += f"</tr>"

        html += "</table>"
    graph_for_stat_average(df, [team_one, team_two], ['fb', 'ft', 'fd', 'fbaron'])


with open('output.html', 'w') as f:
    f.write(html)
