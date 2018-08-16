def get_first_chance(stat, unit, team, df):
    data = df[(df['team'] == team) & (df['player'] == 'Team')]
    got_first = data[data[stat] == unit]

    return (got_first.shape[0] / data.shape[0]) * 100

def fetch_and_display_odds(teams, odds, bookie):
    t1, t2 = list(teams.keys())
    match = odds[( odds['team_1'] == t1 ) & ( odds['team_2'] == t2 )]

    t1_odds = match['team_1_odds'].iloc[0]
    t2_odds = match['team_2_odds'].iloc[0]

    print(t1, "vs", t2, "(" + bookie + ")")
    print("EV for ", t1, teams[t1] * t1_odds)
    print("EV for ", t2, teams[t2] * t2_odds)
    print("\n")


