import pandas as pd
from utils.utils import CovidMongo
import json
import requests
from datetime import datetime, timedelta
# cm = CovidMongo("covid", "state", verbose=False)

# print(type(state.get_all_records()))

# print(state.get_data_by_state("TX"))

# df = cm.get_records_in_df()
# print(df.info())
# print(df.head())
# print(df["Recovered"].sum())


# data = requests.get(url="https://covidtracking.com/api/states").json()
# df = pd.DataFrame(data)
# # print(df.info())
# # print(df.isnull().sum())


# Requests for DailyReports
BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

try:
    todays_date = datetime.now().strftime("%m-%d-%Y")
    csv_url = BASE_URL + todays_date + ".csv"
    df = pd.read_csv(csv_url
                     )
except Exception as ex:
    previous_day_date = datetime.now() - timedelta(days=1)
    previous_day_date = previous_day_date.strftime("%m-%d-%Y")
    csv_url = BASE_URL + previous_day_date + ".csv"
    df = pd.read_csv(csv_url
                     )

# us_state_abbrev = {
#     'Alabama': 'AL',
#     'Alaska': 'AK',
#     'Arizona': 'AZ',
#     'Arkansas': 'AR',
#     'California': 'CA',
#     'Colorado': 'CO',
#     'Connecticut': 'CT',
#     'Delaware': 'DE',
#     'District of Columbia': 'DC',
#     'Florida': 'FL',
#     'Georgia': 'GA',
#     'Guam': 'GU',
#     'Hawaii': 'HI',
#     'Idaho': 'ID',
#     'Illinois': 'IL',
#     'Indiana': 'IN',
#     'Iowa': 'IA',
#     'Kansas': 'KS',
#     'Kentucky': 'KY',
#     'Louisiana': 'LA',
#     'Maine': 'ME',
#     'Maryland': 'MD',
#     'Massachusetts': 'MA',
#     'Michigan': 'MI',
#     'Minnesota': 'MN',
#     'Mississippi': 'MS',
#     'Missouri': 'MO',
#     'Montana': 'MT',
#     'Nebraska': 'NE',
#     'Nevada': 'NV',
#     'New Hampshire': 'NH',
#     'New Jersey': 'NJ',
#     'New Mexico': 'NM',
#     'New York': 'NY',
#     'North Carolina': 'NC',
#     'North Dakota': 'ND',
#     'Northern Mariana Islands': 'MP',
#     'Ohio': 'OH',
#     'Oklahoma': 'OK',
#     'Oregon': 'OR',
#     'Pennsylvania': 'PA',
#     'Puerto Rico': 'PR',
#     'Rhode Island': 'RI',
#     'South Carolina': 'SC',
#     'South Dakota': 'SD',
#     'Tennessee': 'TN',
#     'Texas': 'TX',
#     'Utah': 'UT',
#     'Vermont': 'VT',
#     'Virgin Islands, U.S.': 'VI',
#     'Virginia': 'VA',
#     'Washington': 'WA',
#     'West Virginia': 'WV',
#     'Wisconsin': 'WI',
#     'Wyoming': 'WY',
# }


def wrangle(df):

    # Extract US
    df = df[df['Country/Region'] == 'US']
    # Remove Cruise Ships
    df = df[~ (df["Province/State"].str.endswith("Princess"))]
    # Re-order columns
    df = df[['Province/State', 'Country/Region', 'Latitude', 'Longitude', 'Confirmed',
             'Deaths', 'Recovered', 'Last Update']]
    # Parse datetime
    df["Last Update"] = pd.to_datetime(
        df["Last Update"], infer_datetime_format=True)
    return df


df_usa = wrangle(df)
print(df_usa.head())


# data = requests.get("https://covidtracking.com/api/states/info").json()

# parse_data = []
# for row in data:
#     twitter_user_data = {}
#     twitter_user_data['State'] = row['state']
#     twitter_handle = row['twitter']
#     if twitter_handle:
#         twitter_handle = twitter_handle[1:]
#     twitter_user_data['Username'] = twitter_handle
#     parse_data.append(twitter_user_data)

# # print(parse_data)
# print("Total States: ", len(parse_data))

# cm = CovidMongo(db_name="covid", collection_name="twitter", verbose=True)

# cm.dump_json_data_to_collection(parse_data, verbose=True)
