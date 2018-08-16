I wanted to learn more about pandas, a popular Python data handling library, and to motivate myself, I used the League of Legends dataest provided by Oracle's Elixir to do some simple data handling.

The data can be found [here](http://oracleselixir.com/match-data/).

## Introduction

The goal will be to create a function that can display the games a team played, the opponent, and some useful information. The challnge comes from the fact that each row presents data from a single team's point of view. The data is effectively duplicated again from the opponent's view. For example, a single row looks like:'

```
| gameid | date | week | gamelength | ... |
```

But no `opponent` field. We can get the `opponent` by joining on the `gameid` field.

## Getting the Team's Games

Let's start by getting all the `gameid` that relevant to a team, which we will pass as a command line argument. The program will run like this: `python3 team_games.py "Team Liquid"`.

```python
import sys
import pandas as pd

team = sys.argv[1]
df = pd.read_csv("data.csv")

fields = 'gameid date week game team side gamelength result teamkills teamdeaths'.split()
team_games = df[df['team'] == team].drop_duplicates(subset=['gameid'])[fields]
team_game_ids = team_games['gameid']
```

`data.csv` is the data from Oracle's Elixir. It is an excel spreadsheet, so I had to open it, then export is as a `.csv` file, so I could read it using pandas.

We startt by getting any games where the `team` column is the team we passed in as the first argument. Each game is displayed 10 times, once for each player on each team. We don't care about individual players for this program, so we drop any duplicated `gameid` rows using `drop_duplicates` and passing the `gameid` as a subset. Next we grab just the `gameid` column. This will be useful for performing the join later.

## Get the Team's Opponents

Now we will get all rows that were in any of the games played by the team. This will include the opponents:

```pythong
games = df.loc[df['gameid'].isin(team_game_ids)]
unique_fields = ['gameid']
opponents = games[games['team'] != team].drop_duplicates(subset=unique_fields)[['gameid', 'team']]
opponents.columns = ['gameid', 'opponent']
```

We then proceed to do the reverse logic to the first step: get the rows where the team is _not_ the team we passed in. This time, we only want the `gameid` and `team` This time, we only want the `gameid` and `team`. We will also rename the columns, since otherwise we will end up with two `team` columns.

Lastly, we join the data on the `gameid` column. We will also move the `opponent` column to be directly next to the `team` column. Since you can't have two columns with the same name, I had to rename `opponent` to `the_opponent` when reinserting the column at a different location.

```python
result = pd.merge(team_games, opponents, on='gameid')

result.insert(5, 'the_opponent', result['opponent'])
result.drop('opponent', axis=1, inplace=True)
print(result)
```

Running this with `python3 team_games.py "Echo Fox"` gives me:

```
        gameid  week  game      team  side          the_opponent  gamelength  result  teamkills  teamdeaths
0   1002620109   1.0     2  Echo Fox   Red         Clutch Gaming   32.430000       1       15.0        15.0
1   1002620050   1.0     1  Echo Fox  Blue              FlyQuest   23.833333       1       18.0        13.0
2   1002650038   2.0     1  Echo Fox   Red          OpTic Gaming   38.900000       0        9.0        15.0
3   1002650084   2.0     2  Echo Fox  Blue      Golden Guardians   34.733333       1       23.0        13.0
4   1002650117   3.0     1  Echo Fox   Red           Team Liquid   22.300000       0        7.0        28.0
5   1002650174   3.0     2  Echo Fox   Red                Cloud9   37.366667       1       20.0        18.0
6   1002670206   4.0     1  Echo Fox  Blue  Counter Logic Gaming   36.483333       0        5.0        25.0
7   1002670249   4.0     2  Echo Fox   Red          Team SoloMid   31.950000       1       10.0         4.0
8   1002660285   5.0     1  Echo Fox  Blue           100 Thieves   41.066667       0       10.0        20.0
9   1002660352   5.0     2  Echo Fox   Red      Golden Guardians   32.383333       1       10.0        11.0
10  1002690019   6.0     1  Echo Fox  Blue              FlyQuest   25.916667       1       13.0         3.0
11  1002690064   6.0     2  Echo Fox   Red                Cloud9   36.083333       0       13.0        13.0
12  1002680110   7.0     1  Echo Fox   Red  Counter Logic Gaming   40.600000       1       18.0        17.0
13  1002680146   7.0     2  Echo Fox  Blue          Team SoloMid   43.583333       1       14.0        14.0
14  1002710017   8.0     1  Echo Fox   Red           100 Thieves   28.633333       0        4.0        16.0
15  1002710059   8.0     2  Echo Fox  Blue          OpTic Gaming   36.416667       0        9.0        10.0
```

Great! The next step is to do some analysis, and maybe make some visualisations.
