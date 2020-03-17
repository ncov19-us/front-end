import pandas as pd
from utils.utils import CovidMongo
import json
import requests

cm = CovidMongo("covid", "state", verbose=False)

# print(type(state.get_all_records()))

# print(state.get_data_by_state("TX"))

# df = cm.get_records_in_df()
# print(df.info())
# print(df.head())
# print(df["Recovered"].sum())


data = requests.get(url="https://covidtracking.com/api/states").json()
df = pd.DataFrame(data)
# print(df.info())
# print(df.isnull().sum())


def custom_text(txt):
    return
