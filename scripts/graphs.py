import matplotlib.pyplot as plt
import numpy as np
from data_utils import team_games
from common import get_first_chance

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
        print(team_df)
        running_wins = np.cumsum(team_df.result)
        team_name = team_df.iloc[0].team
        plt.plot(np.arange(1, team_df.shape[0]+1), running_wins, label=team_name)
        plt.legend()

    plt.title("Running victories")

    return plt

def average_first_stat(df, teams, stat):
    for team in teams:
        averages = []
        firsts = 0.0
        games = team_games(df, team)
        for i in range(games.shape[0]):
            firsts += games.iloc[i][stat]
            averages.append(firsts / (i+1))

        print(games.shape[0]+1, len(averages))
        plt.plot(np.arange(1, games.shape[0]+1), averages, label=team)
    plt.ylim(0, 1.05)

    plt.title(stat + "% over last n games")
    plt.legend()
    plt.show()

def running_first_stat(df, teams, stat):
    for team in teams:
        games = team_games(df, team)
        total_games = games.shape[0]
        chance = []
        print(team, stat,"% over last n games")
        for i in range(0, total_games):
            fb_chance = get_first_chance(stat, 1.0, team, df, total_games-i)
            chance.append(fb_chance)
            print(total_games-i, "\t", round(fb_chance, 2))

        plt.plot(np.arange(1, total_games+1), chance, label=team)
    plt.ylim(0, 105)
    plt.title(stat + "% over last n games")
    plt.legend()
    plt.show()
        #print(team, games_played)
        #get_first_chance(stat, unit, team, df, last_n_games=-1):

