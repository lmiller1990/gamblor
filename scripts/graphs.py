import matplotlib.pyplot as plt
import numpy as np
from scripts.data_utils import team_games

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

