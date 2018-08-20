import sys
from data_utils import load_and_clean_data
from graphs import running_victories
from common import get_first_chance, get_ev, relative_odds
from stats import team_medians_kill_and_team

program_to_run = sys.argv[1]
teams = sys.argv[2:]

df = load_and_clean_data()

"""
Running victories

Example: 
    $ python3 scripts/cli.py running_victories "echo fox" "team liquid"

Shows a graph of the running victories for n teams
"""
if program_to_run == 'running_victories':
    plt = running_victories(df, teams=teams)
    plt.show()

"""
Win percentage

Example:
    $ python3 scripts/cli.py win_percentage "echo fox" "team liquid"

% win rate for two teams, and straight average win rate between them.
"""
if program_to_run == 'win_percentage':
    t1_win_chance = get_first_chance('result', 1.0, teams[0], df)/100
    t2_win_chance = get_first_chance('result', 1.0, teams[1], df)/100
    print(relative_odds(t1_win_chance, t2_win_chance))

"""
Kills

Example:
    $ python3 scripts/cli.py kills "fenerbahce esports" "hwa gaming"

Output:
    fenerbahce esports
    k: 13.0 d: 14.0

    hwa gaming
    k: 11.5 d: 13.0

    Total k/d: 24.5 27.0

Show median k/d for two teams, and combined average kills.
"""
if program_to_run == 'kills':
    total_kills = 0
    total_deaths = 0
    for team in teams:
        [k, d] = team_medians_kill_and_team(df, team)
        [k, d] = team_medians_kill_and_team(df, team)
        print(team) 
        print("k:", k, "d:", d, "\n")
        total_kills += k
        total_deaths += d

    print("Total k/d:", total_kills, total_deaths)

if 'first' in program_to_run:
    market = sys.argv[1].split('-')[1]
    t1_win_chance = get_first_chance(market, 1.0, teams[0], df)/100
    t2_win_chance = get_first_chance(market, 1.0, teams[1], df)/100
    print(t1_win_chance, t2_win_chance)
    print(relative_odds(t1_win_chance, t2_win_chance))
