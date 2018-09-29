import sys
import argparse
from data_utils import load_and_clean_data, history
from graphs import running_victories, running_first_stat, average_first_stat
from common import get_first_chance, fetch_and_display_odds
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--teams", help="teams to include in analysis")
parser.add_argument("--markets", help="markets to include in analysis")
parser.add_argument("--scripts", help="script to run")
parser.add_argument("--exclude", help="teams to exlude from calcs", default='')
parser.add_argument("--league", help="league to query by", default=None)
parser.add_argument("--data", help="csv to use for data", default='data.csv')
parser.add_argument("--opponent", help="opponent for use with history", default=None)
parser.add_argument("--stats", 
        help='stat you are interested in. Avail: fb, ft, fd, fbaron',
        default='fb,fd,ft,fbaron')
parser.add_argument("--past_games", help='past n games to get data for', default='-1,8,4')

args = parser.parse_args()

df = load_and_clean_data(data=args.data, league=args.league)
exclude = args.exclude.split(',')
#df = df[~df.opponent.isin(exclude)]
the_teams = args.teams.split(',')

if 'first_to_market' in args.scripts:

    for stat in args.stats.split(','):
        odds_csv = pd.read_csv('odds/' + stat +  '/bet365.csv')
        for i in range(odds_csv.shape[0]):
            teams = [ odds_csv.iloc[i]['team_1'], odds_csv.iloc[i]['team_2'] ]
            if teams[0] in the_teams or teams[1] in the_teams:

                for n in args.past_games.split(','):
                    ft_chances = {}
                    for team in teams:
                        ft_percent = get_first_chance(
                                stat=stat, 
                                unit=1.0, 
                                team=team, 
                                df=df,
                                last_n_games=int(n))
                        ft_chances[team] = ft_percent

                    team_0, team_1 = teams[0], teams[1]

                    last_n_games = "last " + str(n) if int(n) > 0 else "all time"
                    print("\n===", team_0, "vs", team_1, "-", stat, last_n_games, "games ===")

                    relative_odds = {}
                    relative_odds[team_0] = (ft_chances[team_0] + (100 - ft_chances[team_1])) / 200
                    relative_odds[team_1] = (ft_chances[team_1] + (100 - ft_chances[team_0])) / 200
                    print("Relative %\t", round(relative_odds[team_0] * 100, 2), ":", round(relative_odds[team_1] * 100, 2))

                    fetch_and_display_odds(relative_odds, odds_csv, 'bet365', stat)

if 'running_victories' in args.scripts:
    plt = running_victories(df, teams=args.teams.split(','))
    plt.show()

if 'first-av' in args.scripts:
    stats = ['fb', 'ft', 'fd', 'fbaron']
    fig, ax = plt.subplots(nrows=2, ncols=2)
    i = 0
    for row in ax:
        for col in row:
            col.set_ylim([0, 100])
            for team in args.teams.split(','):
                col.set_title(stats[i] + "% (all-time av)")
                [total_games, chance] = average_first_stat(df, team, stats[i])

                col.plot(np.arange(1, total_games+1), np.array(chance) * 100, label=team)
            i = i + 1

    plt.legend()
    fig.tight_layout()
    plt.show()

if 'first-running' in args.scripts:
    stats = ['fb', 'ft', 'fd', 'fbaron']
    fig, ax = plt.subplots(nrows=2, ncols=2)
    i = 0
    for row in ax:
        for col in row:
            col.set_ylim([0, 100])
            for team in args.teams.split(','):
                col.set_title(stats[i] + "% (moving av)")
                [total_games, chance] = running_first_stat(df, team, stats[i])

                col.plot(np.arange(1, total_games+1), chance, label=team)
            i = i + 1

    plt.legend()
    fig.tight_layout()
    plt.show()


if 'history' in args.scripts:
    for team in args.teams.split(','):
        print(history(df, team, args.opponent))

