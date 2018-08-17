import sys
import pandas as pd
from data_utils import load_data
from common import get_first_chance

team = sys.argv[1]
df = pd.read_csv("data.csv")

ft_percent = get_first_chance(
        stat="ft",
        unit=1.0,
        team=team,
        df=df)

print(ft_percent)
