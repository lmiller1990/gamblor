Analysing League of Legends dataset with pandas and python3

In this article, I demonstrate some basic techinques using the pandas data analytics library for python3. I will be using the League of Legends 2018 Summer Split data from Oracle's Elixir.

## Viewing Stats about a Single Team

First, I'd like to be able to view the past games for a team, and some interesting data about them. The way the dataset is set up is each game appears twice, once from the viewpoint of each team. 

For example, say we are reviewing Echo Fox vs Clutch Gaming, with a `gameid` of `1002620109`. There will be two rows; from Echo Fox's point of view, they got 10 kills and suffered 5 deaths. To Clutch Gaming, that is 5 kills and 10 deaths. Data for each player is shown in a single row, which means 10 rows for each game, plus an extra two for the "team", which shows things like `teamkills` and `teamdeaths`. In this case the `player` field is simply `Team`.

This means to get both partipants in a single row, some work is required. Firstly, some basic cleaning of the data is in order:

```python
def load_and_clean_data():
    df = pd.read_csv("data.csv")

    df.team = df.team.str.lower()
    df.league = df.league.str.lower()
    return df.replace({ "1": 1.0, "0": 0.0, 1: 1.0, 0: 0.0, 'Blue': 0.0, 'Red': 1.0 })
```

Some of the 0 and 1 values, for example first blood, are saved as strings instead of numbers. I convert them all to floats, and also set `blue` and `red` to be integer values.

Next, geta all the games for a single team, with a `team_games` method.

```python
def team_games(df, team):
    """
    Returns all unique games played by a team.

    Arguments:
      df: the dataframe containing the data.
      team: the team you are interested in. Eg: "Echo Fox"
    """
    return df[
                ( df['team'] == team ) & 
                ( df['player'] == 'Team' )
            ].drop_duplicates(subset=['gameid'])

```

Running this gives a table like this:

```
        team player  teamkills  teamdeaths
team solomid   Team       14.0         9.0
team solomid   Team       15.0         4.0
team solomid   Team        7.0        20.0
```

With a ton more data. Now we want the opposite of `team_games`, `opponent_games`:

```python
def opponent_games(df, team, gameids):
    """
    Returns opponents for a given team.

    Arguments:

    df: the dataframe containing the data.
    team: the team you are interested in.
    games: a array of gameids the team played in.
    """
    games = df[df.gameid.isin(gameids)]
    opponent_games = games[games.team != team].drop_duplicates(subset=['gameid'])[['gameid', 'team']]
    opponent_games.columns = ['gameid', 'opponent']

    return opponent_games
```

Putting it all together:

```python
df = load_and_clean_data()
team_games = team_games(df, 'team solomid')
opponents = opponent_games(df, 'team solomid', team_games.gameid)

result = team_games.merge(opponents, on="gameid")[['week', 'game', 'team', 'opponent', 'side', 'result', 'teamkills', 'teamdeaths']]

print(result)
```

Gives as a nice summary of the results up to date:

```
week  game         team              opponent  side  result  teamkills  teamdeaths
1.0   1.0  team solomid  counter logic gaming   0.0     1.0       14.0         9.0
1.0   2.0  team solomid              flyquest   0.0     1.0       15.0         4.0
2.0   1.0  team solomid         clutch gaming   0.0     0.0        7.0        20.0
2.0   2.0  team solomid           team liquid   1.0     0.0        2.0         9.0
3.0   1.0  team solomid                cloud9   1.0     1.0       17.0        14.0
3.0   2.0  team solomid      golden guardians   1.0     1.0       14.0         4.0
4.0   1.0  team solomid           100 thieves   1.0     0.0        9.0        20.0
4.0   2.0  team solomid              echo fox   0.0     0.0        4.0        10.0
5.0   1.0  team solomid          optic gaming   0.0     0.0        9.0        12.0
5.0   2.0  team solomid         clutch gaming   1.0     1.0       17.0         4.0
6.0   1.0  team solomid                cloud9   0.0     0.0        7.0        16.0
6.0   2.0  team solomid              flyquest   1.0     0.0        4.0         6.0
7.0   1.0  team solomid      golden guardians   0.0     1.0        9.0         5.0
7.0   2.0  team solomid              echo fox   1.0     0.0       14.0        14.0
8.0   1.0  team solomid  counter logic gaming   1.0     1.0        9.0         3.0
8.0   2.0  team solomid           100 thieves   0.0     1.0       12.0        16.0
```

Now we have gotten a feel for the data, let's do some actual analysis.

## First Blood/Turret/Dragon...

Often a strong early game dictates the result - or does it? Let's investigate. We can grab the percentage of first bloods/turrets easily, using our `team_games` function.

```python
fields = ['fb', 'ft', 'fd', 'fbaron']
games = team_games(df, 'team solomid')

for f in fields:
    taken = games[f].sum()
    total = games[f].shape[0]
    print(f + ':\t', taken, "/" , total, taken/total)
```

Which shows us:

```
fb:	 9.0 / 16 0.5625
ft:	 6.0 / 16 0.375
fd:	 6.0 / 16 0.375
fbaron:	 10.0 / 16 0.625
```

There are a number of ways to interpret this: TSM doesn't prioritize dragon? Perhaps they have a weak lanes (thus not often getting first turret)? How about we check out the rest of the league? First, make `games_by_league` and `teams_by_league` functions:

```python
def games_by_league(df, league):
    return df[df.league.isin(league)].drop_duplicates(subset=['gameid', 'team'])

def teams_by_league(df, league="nalcs"):
    data = df[df.league.isin(league)].drop_duplicates(subset=['team'])['team']
    return data.values
```

Now we can loop each team for the stats. Each stat is assigned a key in a dictionary, and the value is an array of the percentage for each team in the category.

```python
fields = ['fb', 'ft', 'fd', 'fbaron']

teams = teams_by_league(df, ['nalcs'])
stats = {}

for f in fields:
    status[f] = []
    for team in teams:
        games = team_games(df, team)
        taken = games[f].sum()
        total = games[f].shape[0]
        stats[f].append(taken/total)

result = pd.DataFrame(stats, index=teams)
```

...or not. We get an error. It turns out one game was cancelled for technical reasons, and since there was no first blood, the column is blank. We can fix this easily, by first changing all whitespace into `np.nan`, then using `dropna` to get rid of those rows.

```python
for f in fields:
    stats[f] = []
    for team in teams:
        games = team_games(df, team)
        games.replace(" ", np.nan, inplace=True)
        taken = games[f].sum()
        total = games[f].shape[0]
        stats[f].append(taken/total)
```

We get this nice table:

```
                          fb      ft      fd  fbaron
team liquid           0.5000  0.3750  0.7500  0.5000
100 thieves           0.5000  0.4375  0.5625  0.5625
team solomid          0.5625  0.3750  0.3750  0.6250
counter logic gaming  0.6875  0.4375  0.3125  0.3125
clutch gaming         0.3125  0.5000  0.4375  0.3750
cloud9                0.5625  0.6875  0.5000  0.6250
golden guardians      0.5625  0.4375  0.6875  0.1250
optic gaming          0.4375  0.5625  0.3125  0.5625
flyquest              0.4375  0.6250  0.4375  0.5000
echo fox              0.3750  0.5625  0.5625  0.5625
```

To get some more context, let's add in the total wins for each team and sort by that:

```python
stats['wins'] = []
for team in teams:
    stats['wins'].append(team_games(df, team).result.sum())

result = pd.DataFrame(stats, index=teams)
print(result.sort_values(by='wins', ascending=False))
```

Now we get:

```
                          fb      ft      fd  fbaron  wins
team liquid           0.5000  0.3750  0.7500  0.5000  11.0
100 thieves           0.5000  0.4375  0.5625  0.5625  10.0
cloud9                0.5625  0.6875  0.5000  0.6250   9.0
flyquest              0.4375  0.6250  0.4375  0.5000   9.0
echo fox              0.3750  0.5625  0.5625  0.5625   9.0
team solomid          0.5625  0.3750  0.3750  0.6250   8.0
optic gaming          0.4375  0.5625  0.3125  0.5625   8.0
clutch gaming         0.3125  0.5000  0.4375  0.3750   6.0
counter logic gaming  0.6875  0.4375  0.3125  0.3125   5.0
golden guardians      0.5625  0.4375  0.6875  0.1250   5.0
```

First baron is pretty consistent in the top 7. All of them are within three games of each other, but I did expect a bit or a larger gap. First dragon, turret and blood appears completely non correlated though (we will see this is indeed not highly correlated later on, using pandas `corr` method). Golden Guardians is a bit of an outliner - a lot of first dragons, second only to Team Liquid. This could be for a number of reasons, such as the type of dragon, or some teams favoring early game junglers, for example.

## Using `corr` to find correlation

Let's see if there is a relationship between first dragon, turret, etc, and actually winning the game.
