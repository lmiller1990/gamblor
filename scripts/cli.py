import sys
import argparse
from data_utils import load_and_clean_data
from graphs import running_victories, running_first_stat, average_first_stat
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--teams", help="teams to include in analysis")
parser.add_argument("--markets", help="markets to include in analysis")
parser.add_argument("--scripts", help="script to run")
parser.add_argument("--stat", help="script to run")

args = parser.parse_args()

df = load_and_clean_data()

if 'running_victories' in args.scripts:
    plt = running_victories(df, teams=args.teams.split(','))
    plt.show()

if 'first-av' in args.scripts:
    stats = ['fb', 'ft', 'fd', 'fbaron']
    fig, ax = plt.subplots(nrows=2, ncols=2)
    i = 0
    for row in ax:
        for col in row:
            for team in args.teams.split(','):
                col.set_title(stats[i] + "%")
                [total_games, chance] = average_first_stat(df, team, stats[i])

                col.plot(np.arange(1, total_games+1), chance, label=team)
            i = i + 1

    plt.ylim(0, 1.)
    plt.legend()
    fig.tight_layout()
    plt.show()

if 'first-running' in args.scripts:
    stats = ['fb', 'ft', 'fd', 'fbaron']
    fig, ax = plt.subplots(nrows=2, ncols=2)
    i = 0
    for row in ax:
        for col in row:
            for team in args.teams.split(','):
                col.set_title(stats[i] + "%")
                [total_games, chance] = running_first_stat(df, team, stats[i])

                col.plot(np.arange(1, total_games+1), chance, label=team)
            i = i + 1

    plt.legend()
    fig.tight_layout()
    plt.show()

