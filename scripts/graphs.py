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

    return plt

def running_first_bloods(df, teams):
    for team in teams:
        games = team_games(df, team)
        total_games = games.shape[0]
        chance = []
        print(team, "Fbaron% over last n games")
        for i in range(0, total_games):
            fb_chance = get_first_chance('fbaron', 1.0, team, df, total_games-i)
            chance.append(fb_chance)
            print(total_games-i, "\t", round(fb_chance, 2))

            
        plt.plot(np.arange(1, total_games+1), chance, label=team)
        plt.ylim(0, 105)
    plt.title("fd% over last n games")
    plt.legend()
    plt.show()
        #print(team, games_played)
        #get_first_chance(stat, unit, team, df, last_n_games=-1):

