import pandas as pd

def load_data(path, csv):
    df = pd.read_csv("data.csv")
    odds = pd.read_csv(path + "/" + csv)
    return df, odds

