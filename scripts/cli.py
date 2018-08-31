import sys
import argparse
from data_utils import load_and_clean_data
from graphs import running_victories, running_first_stat, average_first_stat

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
    average_first_stat(df, args.teams.split(','), args.stat)

if 'first-running' in args.scripts:
    running_first_stat(df, args.teams.split(','), args.stat)
