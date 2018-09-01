from data_utils import team_games
from common import get_first_chance
import matplotlib.pyplot as plt
import numpy as np

def running_victories(df, teams):
    """
    Show a graph of the team's running victory count.

    Arguments:
        df: the dataframe with the data.
        teams: an array of teams. Eg: ['echo fox', 'team liquid']

    Example: 
        running_victories(teams=['echo fox', 'cloud9'], df=df)
    """
    get_game = lambda team: team_games(df, team)

    victories_for_teams = list(map(get_game, teams))

    for team_df in victories_for_teams:
        running_wins = np.cumsum(team_df.result)
        team_name = team_df.iloc[0].team
        plt.plot(np.arange(1, team_df.shape[0]+1), running_wins, label=team_name)
        plt.legend()

    plt.title("Running victories")

    return plt

def average_first_stat(df, team, stat):
    averages = []
    firsts = 0.0
    games = team_games(df, team)
    games.dropna(inplace=True)
    for i in range(games.shape[0]):
        firsts += games.iloc[i][stat]
        averages.append(firsts / (i+1))
    
    return [ games.shape[0], averages ]


def running_first_stat(df, team, stat):
    games = team_games(df, team)
    total_games = games.shape[0]
    games.dropna(inplace=True)
    chance = []

    for i in range(0, total_games):
        fb_chance = get_first_chance(stat, 1., team, df, total_games-i)
        chance.append(fb_chance)

    return [total_games, chance]
