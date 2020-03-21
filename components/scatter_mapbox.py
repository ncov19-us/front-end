from datetime import datetime, timedelta
import pandas as pd

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq

from utils.settings import BASE_URL, MAPBOX_ACCESS_TOKEN

px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

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


########################################################################
#
# App Callbacks
#
########################################################################



# @app.callback(Output("us-map", "figure"), [Input("map-input", "value")])
def scatter_mapbox() -> dbc.Card:
    """Displays choroplepth map for the data. For the whole US, the map is divided by state.
    TODO: For individual states,the map will be divided by county lines. Add callbacks

    :return card: A dash boostrap component Card object with a dash component Graph inside drawn using plotly express scatter_mapbox
    :rtype: dbc.Card
    """
    color_scale = ["#ffbaba", "#ff7b7b", "#ff5252", "#ff0000", "#a70000"]
    fig = px.scatter_mapbox(
        daily_reports,
        lat="Latitude",
        lon="Longitude",
        color="Confirmed",
        size="Confirmed",
        size_max=35,
        hover_name="Province/State",
        hover_data=["Confirmed", "Deaths", "Recovered", "Province/State"],
        color_continuous_scale=color_scale,
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # This takes away the colorbar on the right hand side of the plot
        coloraxis_showscale=False,
        mapbox_style="dark",
        mapbox=dict(center=dict(lat=39.8097343, lon=-98.5556199), zoom=3),
    )

    # https://community.plot.ly/t/plotly-express-scatter-mapbox-hide-legend/36306/2
    # print(fig.data[0].hovertemplate)
    # <b>%{hovertext}</b><br><br>Confirmed=%{marker.color}\\
    # <br>Deaths=%{customdata[1]}<br>Recovered=%{customdata[2]}<br>Latitude=%{lat}<br>Longitude=%{lon}
    fig.data[0].update(
        hovertemplate="%{customdata[3]}<br>Confirmed: %{marker.size}<br>Deaths: %{customdata[1]}<br>Recovered: %{customdata[2]}"
    )

    card = dbc.Card(dbc.CardBody(dcc.Graph(figure=fig, style={"height": "54vh"})))
    return card

    