from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import flask
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

from app import cache
from utils.settings import (
    MAPBOX_ACCESS_TOKEN,
    DRIVE_THRU_URL,
    NCOV19_API,
    MAPBOX_STYLE,
    STATES_COORD,
)
import requests


px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)


# TODO: Make Drive-thru testing center API
def get_drive_thru_testing_centers():
    try:
        drive_thru_df = pd.read_csv(DRIVE_THRU_URL)
    except Exception as ex:
        print(ex)
    return drive_thru_df


########################################################################
#
# App Callbacks
#
########################################################################


def confirmed_scatter_mapbox(state="US"):
    """Displays choroplepth map for the data. For the whole US, the map is divided by state.
    TODO: For individual states,the map will be divided by county lines. Add callbacks

    :return card: A dash boostrap component Card object with a dash component Graph inside drawn using plotly express scatter_mapbox
    :rtype: dbc.Card
    """
    URL = NCOV19_API + "county"
    response = requests.get(URL).json()
    data = response["message"]
    data = pd.read_json(data, orient="records")
    data["State Name"] = data["State Name"].str.title()
    data["County Name"] = data["County Name"].str.title()

    color_scale = [
        "#FA9090",
        "#F77A7A",
        "#F56666",
        "#F15454",
        "#ED4343",
        "#E93535",
        "#E42828",
        "#DE1E1E",
        "#D71515",
        "#CF0D0D",
        "#C70707",
        "#BD0202",
        "#B30000",
        "#A90000",
        "#9E0000",
        "#920000",
        "#870000",
    ]

    # data["log_confirmed"] = np.log(data["Confirmed"] + 0.1 ** 10)
    # data["log_confirmed"] = (data["Confirmed"] - data["Confirmed"].min()) / (
    #    data["Confirmed"].max() - data["Confirmed"].min()
    # )
    # normalized_df=(df-df.min())/(df.max()-df.min())#
    # set lat/long
    if state == "US":
        lat, lon, zoom = 39.8097343, -98.5556199, flask.session["zoom"]
    else:
        lat, lon, zoom = (
            STATES_COORD[state]["latitude"],
            STATES_COORD[state]["longitude"],
            STATES_COORD[state]["zoom"],
        )

    fig = px.scatter_mapbox(
        data,
        lat="Latitude",
        lon="Longitude",
        color="Confirmed",
        size="Confirmed",  # "log_confirmed",
        size_max=50,
        hover_name="County Name",
        hover_data=["Confirmed", "Death", "State Name", "County Name"],
        color_continuous_scale=color_scale,
    )

    fig.layout.update(
        # Title still no show after this
        title="Corona Virus Cases in U.S.",
        title_x=0.1,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # This takes away the colorbar on the right hand side of the plot
        coloraxis_showscale=False,
        mapbox_style=MAPBOX_STYLE,
        mapbox=dict(
            center=dict(lat=lat, lon=lon), zoom=zoom
        ),  # flask.session["zoom"]),
    )

    # https://community.plot.ly/t/plotly-express-scatter-mapbox-hide-legend/36306/2
    # print(fig.data[0].hovertemplate)
    fig.data[0].update(
        hovertemplate="%{customdata[3]}, %{customdata[2]}<br>Confirmed: %{marker.size}<br>Deaths: %{customdata[1]}"
    )

    return fig


def drive_thru_scatter_mapbox(state="US"):
    """DO NOT CACHE. NEED APP_STATE TO CHANGE DYNAMICALLY
    """

    # set lat/long
    if state == "US":
        lat, lon, zoom = 39.8097343, -98.5556199, flask.session["zoom"]
    else:
        lat, lon, zoom = (
            STATES_COORD[state]["latitude"],
            STATES_COORD[state]["longitude"],
            STATES_COORD[state]["zoom"],
        )
    # print(state)
    # print(lat, lon, zoom)

    fig = px.scatter_mapbox(
        get_drive_thru_testing_centers(),
        lat="Latitude",
        lon="Longitude",
        hover_name="Name",
        hover_data=["URL"],
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style=MAPBOX_STYLE,
        mapbox=dict(center=dict(lat=lat, lon=lon), zoom=zoom,),
        dragmode=False,
    )

    fig.data[0].update(
        hovertemplate="<b><a href='%{customdata[0]}' style='color:black'>%{hovertext}</a></b>",
        marker={"size": 30, "symbol": "marker"},
    )

    return fig
