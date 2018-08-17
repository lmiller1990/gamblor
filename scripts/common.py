def get_first_chance(stat, unit, team, df):
    data = df[(df['team'] == team) & (df['player'] == 'Team')]
    got_first = data[data[stat] == unit]

    return (got_first.shape[0] / data.shape[0]) * 100

def get_ev(percent_to_get, bookie_odds):
    return percent_to_get * bookie_odds

def fetch_and_display_odds(teams, odds, bookie, market, evs_by_bookies):
    t1, t2 = list(teams.keys())
    match = odds[( odds['team_1'] == t1 ) & ( odds['team_2'] == t2 )]

    t1_odds = match['team_1_odds'].iloc[0]
    t2_odds = match['team_2_odds'].iloc[0]

    print("[" + market + "]")
    print(t1, "vs", t2, "(" + bookie + ")")
    t1_ev = get_ev(teams[t1], t1_odds)
    t2_ev = get_ev(teams[t2], t2_odds)
    print("EV for ", t1, t1_ev, "<------------------- High EV" if t1_ev > 1.1 else  "")
    print("EV for ", t2, t2_ev, "<------------------- High EV" if t2_ev > 1.1 else  "")

    if bookie in evs_by_bookies:
        pass
        if market in evs_by_bookies[bookie]:
            pass
        else:
            evs_by_bookies[bookie][market] = []
    else:
        evs_by_bookies[bookie] = {}
        evs_by_bookies[bookie][market] = []

    # evs_by_bookies[bookie][market].append({ 'match': t1 + ' vs ' + t2, 'odds': {  })

    return evs_by_bookies

