import pandas as pd

df = pd.read_csv('my_bets/historical-Table 1.csv')
df = df.dropna(subset=['favored_win'])
df.t1 = df.t1.str.lower()
df.t1 = df.t1.str.strip()
df.t2 = df.t2.str.lower()
df.t2 = df.t2.str.strip()

def favored_stats_by_market(df, market):
    total = df[df.market == market].shape[0]
    won = df[(df.market == market) & (df.favored_win == True)].shape[0]

    return [won, total]

def simulate(df, market, amt_bet, on_favorite):
    total = df[df.market == market]
    won = df[(df.market == market) & (df.favored_win == on_favorite)]
    
    winnings = won['t1_odds'] * amt_bet
    invested = (total.shape[0] * amt_bet)
    profit = winnings.sum() - invested
    percent_profit = profit/(amt_bet * total.shape[0]) * 100

    return round(percent_profit, 2)

def filter_by_teams(df, team): return df[(df.t1 == team) | (df.t2 == team)]

#for market in ['fb', 'ft', 'fd', 'fbaron', 'win']:
#    the_df = df  # filter_by_teams(df, team)
#    print('games played', the_df.shape[0]/5)
#    print(market)
#    print('Bet on favorite     ', simulate(the_df, market, 10, True))
#    print('Bet against favorite', simulate(the_df, market, 10, False))

def by_teams(t1, t2):
    for market in ['fb', 'ft', 'fd', 'fbaron', 'win']:
        for team in [t1, t2]:
            print("\n", team)
            the_df = filter_by_teams(df, team)
            print('games played', the_df.shape[0]/5)
            print(market)
            print('Bet on favorite     ', simulate(the_df, market, 10, True))
            print('Bet against favorite', simulate(the_df, market, 10, False))


by_teams('gambit esports', 'kaos latin gamers')
