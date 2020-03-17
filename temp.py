import pandas as pd
from utils.utils import CovidMongo
import json

cm = CovidMongo("covid", "state", verbose=False)

# print(type(state.get_all_records()))

# print(state.get_data_by_state("TX"))


print(cm.get_records_in_df())
