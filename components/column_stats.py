import requests
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"


# TODO: Remove logic from here and put it to AWS Lambda
try:
    todays_date = datetime.now().strftime("%m-%d-%Y")
    csv_url = BASE_URL + todays_date + ".csv"
    daily_reports = pd.read_csv(csv_url)
except Exception as ex:
    previous_day_date = datetime.now() - timedelta(days=1)
    previous_day_date = previous_day_date.strftime("%m-%d-%Y")
    csv_url = BASE_URL + previous_day_date + ".csv"
    daily_reports = pd.read_csv(csv_url)


def wrangle(df) -> pd.DataFrame:
    # Extract US
    df = df[df["Country/Region"] == "US"]
    # Remove Cruise Ships
    df = df[~(df["Province/State"].str.endswith("Princess"))]
    # Re-order columns
    df = df[
        [
            "Province/State",
            "Country/Region",
            "Latitude",
            "Longitude",
            "Confirmed",
            "Deaths",
            "Recovered",
            "Last Update",
        ]
    ]
    # Parse datetime
    df["Last Update"] = pd.to_datetime(df["Last Update"], infer_datetime_format=True)
    return df


daily_reports = wrangle(daily_reports)

def states_confirmed_stats(state=None) -> dbc.ListGroup:
    """    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """
    list_group = dbc.ListGroup(
       [
            dbc.ListGroupItem(
                [

                    html.P([
                        html.Span(f"{daily_reports.iloc[i]['Confirmed']}", className="states-stats-confirmed-list-num"),
                        html.Span(f"   {daily_reports.iloc[i]['Province/State']}", className="states-stats-confirmed-list-state"),
                        ],
                        className="states-stats-confirmed-list-txt",
                    ),
                ],
                className="states-stats-confirmed-list-item",
            )
            for i in range(min(len(daily_reports), 60))
        ],
        flush=True,
        className="states-stats-confirmed-listgroup",
    )

    return list_group


def states_deaths_stats(state=None) -> dbc.ListGroup:
    """    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """
    list_group = dbc.ListGroup(
       [
            dbc.ListGroupItem(
                [

                    html.P([
                        html.Span(f"{daily_reports.iloc[i]['Deaths']}", className="states-stats-deaths-list-num"),
                        html.Span(f"   {daily_reports.iloc[i]['Province/State']}", className="states-stats-deaths-list-state"),
                        ],
                        className="states-stats-deaths-list-txt",
                    ),
                ],
                className="states-stats-deaths-list-item",
            )
            for i in range(min(len(daily_reports), 60))
        ],
        flush=True,
        className="states-stats-death-listgroup",
    )
    
    return list_group


def states_recovered_stats(state=None) -> dbc.ListGroup:
    """    
    :params state: display news feed for a particular state. If None, display news feed for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """
    list_group = dbc.ListGroup(
       [
            dbc.ListGroupItem(
                [

                    html.P([
                        html.Span(f"{daily_reports.iloc[i]['Recovered']}", className="states-stats-recovered-list-num"),
                        html.Span(f"   {daily_reports.iloc[i]['Province/State']}", className="states-stats-recovered-list-state"),
                        ],
                        className="states-stats-recovered-list-txt",
                    ),
                ],
                className="states-stats-recovered-list-item",
            )
            for i in range(min(len(daily_reports), 60))
        ],
        flush=True,
        className="states-stats-recovered-listgroup",
    )
    
    return list_group

if __name__ == "__main__":
    print(daily_reports)