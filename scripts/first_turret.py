import sys
import os
import pandas as pd
from common import get_first_chance, fetch_and_display_odds
from data_utils import load_data

if __name__ == '__main__':
    csv_dir = sys.argv[1]
    csvs = os.listdir(csv_dir)

    for csv in csvs:
        df, bookie_odds = load_data(csv_dir, csv)
        for i in range(bookie_odds.shape[0]):
            teams = [ bookie_odds.iloc[i]['team_1'], bookie_odds.iloc[i]['team_2'] ]

            ft_chances = {}
            for team in teams:
                ft_percent = get_first_chance(stat='ft', unit=1.0, team=team, df=df)
                print(team, ft_percent)
                ft_chances[team] = ft_percent

            team_0, team_1 = teams[0], teams[1]

            relative_odds = {}
            relative_odds[team_0] = (ft_chances[team_0] + (100 - ft_chances[team_1])) / 200
            relative_odds[team_1] = (ft_chances[team_1] + (100 - ft_chances[team_0])) / 200

            fetch_and_display_odds(relative_odds, bookie_odds, csv.split(".")[0])

