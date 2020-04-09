import requests
import dash_bootstrap_components as dbc
import dash_html_components as html
from utils import REVERSE_STATES_MAP
from utils import config
from app import cache
import pandas as pd


# DEPRECATED?
# TODO: Remove logic from here and put it to AWS Lambda

# worked when i moved this into the try/except in the states_confirmed_stats function
try:
    URL = config.NCOV19_API + config.COUNTY
    response = requests.get(URL).json()
    data = response["message"]

    data = pd.DataFrame.from_records(data)
    data["state_name"] = data["state_name"].str.title()
    # confirmed = data.groupby(["state_name"])["confirmed"].sum()
    # confirmed = confirmed.sort_values(ascending=False).to_dict()

    # death = data.groupby(["state_name"])["death"].sum()
    # death = death.sort_values(ascending=False).to_dict()
    last_updated = data["last_update"][0]

except Exception as ex:
    print(f"[ERROR]: {ex}")


STATES = list(set(data["state_name"].to_list()))

del response, data


# @cache.memoize(timeout=600)
# def states_confirmed_stats(state="United States") -> dbc.ListGroup:
#     """    
#     :params state: display news feed for a particular state. If None, display news feed
#         for the whole US

#     :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
#     :rtype: dbc.ListGroup    
#     """

#     state = REVERSE_STATES_MAP[state]

#     try:
#         URL = config.NCOV19_API + config.COUNTY
#         response = requests.get(URL).json()
#         data = response["message"]

#         data = pd.DataFrame.from_records(data)
#         data["state_name"] = data["state_name"].str.title()

#         if state in ["US", "United States"]:
#             # print('if state', state)
#             confirmed = data.groupby(["state_name"])["confirmed"].sum()
#             confirmed = confirmed.sort_values(ascending=False).to_dict()
#             # print(confirmed)
#         else:
#             # print('else state', state)
#             confirmed = data[data["state_name"] == state]
#             # print(1)
#             confirmed = confirmed[["county_name", "confirmed"]]
#             confirmed = dict(
#                 confirmed.sort_values(by="confirmed", ascending=False).to_records(
#                     index=False
#                 )
#             )

#         del response, data
#     except:
#         print(f"[ERROR] states_confirmed_stats({state}) error accessing ncov19.us API")

#     list_group = dbc.ListGroup(
#         [
#             dbc.ListGroupItem(
#                 [
#                     html.Button(
#                         html.Div(
#                             [
#                                 html.Span(
#                                     f"{value:,d}",
#                                     className="states-stats-confirmed-list-num",
#                                 ),
#                                 html.Span(
#                                     f"     {key}",
#                                     className="states-stats-confirmed-list-state",
#                                 ),
#                             ]
#                         ),
#                         n_clicks=0,
#                         id=f"states-confirmed-{key}",
#                         className="states-stats-confirmed-list-txt",
#                     ),
#                 ],
#                 className="states-stats-confirmed-list-item",
#             )
#             for key, value in confirmed.items()
#         ],
#         flush=True,
#         className="states-stats-confirmed-listgroup",
#     )

#     return list_group


# @cache.memoize(timeout=600)
# def states_deaths_stats(state="US") -> dbc.ListGroup:
#     """    
#     :params state: display news feed for a particular state. If None, display news feed
#         for the whole US

#     :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
#     :rtype: dbc.ListGroup    
#     """

#     try:
#         URL = config.NCOV19_API + config.COUNTY
#         response = requests.get(URL).json()
#         data = response["message"]

#         data = pd.DataFrame.from_records(data)
#         data["state_name"] = data["state_name"].str.title()

#         if state == "US":
#             deaths = data.groupby(["state_name"])["deaths"].sum()
#             deaths = deaths.sort_values(ascending=False).to_dict()
#         else:
#             deaths = data[data["state_name"] == state]
#             deaths = df[["County Name", "Confirmed"]]
#             deaths = dict(
#                 confirmed.sort_values(by="Confirmed", ascending=False).to_records(
#                     index=False
#                 )
#             )

#         del response, data
#     except:
#         print("[ERROR] states_confirmed_stats error accessing ncov19.us API")

#     list_group = dbc.ListGroup(
#         [
#             dbc.ListGroupItem(
#                 [
#                     html.P(
#                         [
#                             html.Span(
#                                 f"{value:,d}", className="states-stats-deaths-list-num",
#                             ),
#                             html.Span(
#                                 f"   {key}", className="states-stats-deaths-list-state",
#                             ),
#                         ],
#                         className="states-stats-deaths-list-txt",
#                     ),
#                 ],
#                 id=f"states-death-{key}",
#                 className="states-stats-deaths-list-item",
#             )
#             for key, value in deaths.items()
#         ],
#         flush=True,
#         className="states-stats-death-listgroup",
#     )

#     return list_group
