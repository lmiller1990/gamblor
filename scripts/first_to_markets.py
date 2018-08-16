import sys
import os
import pandas as pd
from common import get_first_chance, fetch_and_display_odds
from data_utils import load_data

first_to_stats = { 
    'first_blood': { 'stat': 'fb', 'unit': '1', 'data_dir': 'odds/first_blood' },
    'first_turret': { 'stat': 'ft', 'unit': 1.0, 'data_dir': 'odds/first_turret' }
}

for key in first_to_stats:
    csvs = os.listdir("odds/" + key)

    for csv in csvs:
        current_market = first_to_stats[key]
        df, bookie_odds = load_data(current_market['data_dir'], csv)
        for i in range(bookie_odds.shape[0]):
            teams = [ bookie_odds.iloc[i]['team_1'], bookie_odds.iloc[i]['team_2'] ]

            ft_chances = {}
            for team in teams:
                ft_percent = get_first_chance(stat=current_market['stat'], unit=current_market['unit'], team=team, df=df)
                print(key + ' status for', team + ':', ft_percent)
                ft_chances[team] = ft_percent

            team_0, team_1 = teams[0], teams[1]

            relative_odds = {}
            relative_odds[team_0] = (ft_chances[team_0] + (100 - ft_chances[team_1])) / 200
            relative_odds[team_1] = (ft_chances[team_1] + (100 - ft_chances[team_0])) / 200

            fetch_and_display_odds(relative_odds, bookie_odds, csv.split(".")[0])

