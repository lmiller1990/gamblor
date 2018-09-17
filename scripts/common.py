def get_first_chance_all_games(df, team, stat, unit):
    """
    Get average over all previous games
    """
    data = df[(df.team == team) & (df.player == 'Team')]
    num_games = data.shape[0]

    chance_over_all_games = []
    for i in range(num_games):
        num_and_chance = {}
        games = data.tail(num_games - i)
        got_first = games[games[stat] == unit]

        num_and_chance['num_games'] = num_games - i
        num_and_chance['chance'] = got_first.shape[0] / games.shape[0]
        num_and_chance['week_game'] = str(games['week'].iloc[0]) + '-' + str(games['game'].iloc[0])
        chance_over_all_games.append(num_and_chance)

    return chance_over_all_games



def get_first_chance(stat, unit, team, df, last_n_games=-1):
    """
    Get the chance of a 'first' occurrence, such as first blood, first dragon.

    Arguments:

    stat: the event, such as 'fb' for first blood, 'fd' for first dragon
    unit: the unit the stat is. For example "1", 1.0, etc.
    team: the team you are interested in, such as 'Echo Fox'
    df:   the data frame containing the data

    Returns: the percentage chance, as a percentage from 0 - 100.
    """

    data = df[(df.team == team) & (df.player == 'Team')]
    if last_n_games > 0:
        data = data.tail(last_n_games)

    got_first = data[data[stat] == unit]

    return (got_first.shape[0] / data.shape[0]) * 100

def get_ev(percent_to_get, bookie_odds):
    """
    Get the expected value (EV) of a bet w.r.t the bookie odds

    Arguments: 

    percent_to_get: the percentage chance of the event, between 0 - 1
    bookie_odds: the bookie odds.
    
    Returns: the expected value.
    """
    return percent_to_get * bookie_odds

def relative_odds(t1_percent, t2_percent):
    """
    Get the relative odds of two percentages.

    Arguments:
        t1_percent: percentage (between 0-1)
        t2_percent: percentage (between 0-1)

    Returns
        [t1_relative, t2_relative]: straight average between the two percentages.
    """
    return [
            (t1_percent + (1 - t2_percent)) / 2,
            (t2_percent + (1 - t1_percent)) / 2
            ]

def fetch_and_display_odds(teams, odds, bookie, market):
    t1, t2 = list(teams.keys())
    match = odds[( odds['team_1'] == t1 ) & ( odds['team_2'] == t2 )]

    t1_odds = match['team_1_odds'].iloc[0]
    t2_odds = match['team_2_odds'].iloc[0]

    t1_ev = get_ev(teams[t1], t1_odds)
    t2_ev = get_ev(teams[t2], t2_odds)
    print("Odds:", t1_odds, ":", t2_odds)
    print(t1, "\tev:", round(t1_ev, 2), "\t<------------------- High EV" if t1_ev > 1.1 else  "")
    print(t2, "\tev:", round(t2_ev, 2), "\t<------------------- High EV" if t2_ev > 1.1 else  "")
