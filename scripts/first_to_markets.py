import sys
import os
import pandas as pd
from common import get_first_chance, fetch_and_display_odds
from data_utils import load_data, load_and_clean_data

first_to_stats = { 
    'first_blood': { 'stat': 'fb', 'unit': 1.0, 'data_dir': 'odds/first_blood' },
    'first_turret': { 'stat': 'ft', 'unit': 1.0, 'data_dir': 'odds/first_turret' },
    'first_dragon': { 'stat': 'fd', 'unit': 1.0, 'data_dir': 'odds/first_dragon' },
    'first_baron': { 'stat': 'fbaron', 'unit': 1.0, 'data_dir': 'odds/first_baron' }
}

evs_by_bookie = {}

df = load_and_clean_data()
for key in first_to_stats:
    csvs = os.listdir("odds/" + key)

    for csv in csvs:
        current_market = first_to_stats[key]
        bookie_odds = load_data(current_market['data_dir'], csv)
        for i in range(bookie_odds.shape[0]):
            teams = [ bookie_odds.iloc[i]['team_1'], bookie_odds.iloc[i]['team_2'] ]

            for n in [-1, 8, 4]:
                ft_chances = {}
                for team in teams:
                    ft_percent = get_first_chance(
                            stat=current_market['stat'], 
                            unit=current_market['unit'], 
                            team=team, 
                            df=df,
                            last_n_games=n)
                    ft_chances[team] = ft_percent

                team_0, team_1 = teams[0], teams[1]
                print("\n===", team_0, "vs", team_1, "-", key, "last", n, "games ===")
                # print("Overall %\t", str(ft_chances[team_0]), ":", str(ft_chances[team_1]))

                relative_odds = {}
                relative_odds[team_0] = (ft_chances[team_0] + (100 - ft_chances[team_1])) / 200
                relative_odds[team_1] = (ft_chances[team_1] + (100 - ft_chances[team_0])) / 200
                print("Relative %\t", round(relative_odds[team_0] * 100, 2), ":", round(relative_odds[team_1] * 100, 2))

                evs_by_bookie = fetch_and_display_odds(relative_odds, bookie_odds, csv.split(".")[0], key, evs_by_bookie)

