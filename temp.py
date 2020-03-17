
from utils.utils import CovidMongo


state = CovidMongo("covid", "state", verbose=False)

# print(state.get_all_records())

print(state.get_data_by_state("TX"))
