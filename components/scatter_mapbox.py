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
    correct_url = "https://raw.githubusercontent.com/ncov19-us/ds/master/drive_thru_testing_locations/locations-with-addresses.csv"
    try:
        drive_thru_df = pd.read_csv(correct_url)
        drive_thru_df["Addresses"] = drive_thru_df["Addresses"].str.replace(", United States of America","")
        #drive_thru_df["ZIP"] = drive_thru_df["Addresses"].str.split(",").str[-1]
        drive_thru_df["State"] = drive_thru_df["Addresses"].str.split(",").str[-2]
        drive_thru_df["City"] = drive_thru_df["Addresses"].str.split(",").str[-4]
        drive_thru_df["Full Address"] = drive_thru_df["Addresses"].replace(","," ")
        #drive_thru_df["Address"] = drive_thru_df["Addresses"].str.split(",").str[:-4]
    except Exception as ex:
        print(ex)
    return drive_thru_df


########################################################################
#
# App Callbacks
#
########################################################################


def confirmed_scatter_mapbox(state="United States"):
    """Displays choroplepth map for the data. For the whole US, the map is divided by state.
    
    :return card: A dash boostrap component Card object with a dash component Graph inside drawn using plotly express scatter_mapbox
    :rtype: dbc.Card
    """

    URL = NCOV19_API + "county"
    response = requests.get(URL).json()
    data = response["message"]
    data = pd.DataFrame.from_records(data)

    # color_scale = ['#fce9b8', '#fbe6ad','#fbe3a3','#fbdf99',
    #                 '#fadc8f','#fad985','#f9d67a',
    #                 '#f9d370','#f8d066','#f8cc5c','#f8c952',
    #                 '#f7c647','#f7c33d','#f6c033',
    #                 '#f6bd29','#f5b91f','#f5b614','#f4b30a',
    #                 '#F4B000','#efac00','#eaa900','#e5a500','#e0a200','#dc9e00']

    color_scale = ['#fadc8f','#f9d67a',
                    '#f8d066','#f8c952',
                   '#f7c33d',
                    '#f6bd29','#f5b614',
                    '#F4B000','#eaa900','#e0a200','#dc9e00']

    # Scaled the data exponentially to show smaller values.
    data['scaled'] = data["confirmed"] ** 0.77
    
    # set lat/long
    if state == "United States":
        lat, lon, zoom = 39.8097343, -98.5556199, flask.session["zoom"]
    else:
        lat, lon, zoom = (
            STATES_COORD[state]["latitude"],
            STATES_COORD[state]["longitude"],
            STATES_COORD[state]["zoom"],
        )

    fig = px.scatter_mapbox(
        data,
        lat="latitude",
        lon="longitude",
        color="confirmed",
        size="scaled",
        size_max=50,
        hover_name="county_name",
        hover_data=["confirmed", "death", "state_name", "county_name"],
        color_continuous_scale=color_scale,
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # This takes away the colorbar on the right hand side of the plot
        coloraxis_showscale=False,
        mapbox_style=MAPBOX_STYLE,
        mapbox=dict(
            center=dict(lat=lat, lon=lon), 
            zoom=zoom,
        ),
    )

    # https://community.plot.ly/t/plotly-express-scatter-mapbox-hide-legend/36306/2
    # print(fig.data[0].hovertemplate)
    fig.data[0].update(
        hovertemplate="%{customdata[3]}, %{customdata[2]}<br>Confirmed: %{customdata[0]}<br>Deaths: %{customdata[1]}"
    )

    return fig


def drive_thru_scatter_mapbox(state="United States"):
    """DO NOT CACHE. NEED APP_STATE TO CHANGE DYNAMICALLY
    """

    # set lat/long
    if state == "United States":
        lat, lon, zoom = 39.8097343, -98.5556199, flask.session["zoom"]
    else:
        lat, lon, zoom = (
            STATES_COORD[state]["latitude"],
            STATES_COORD[state]["longitude"],
            STATES_COORD[state]["zoom"],
        )

    fig = px.scatter_mapbox(
        get_drive_thru_testing_centers(),
        lat="Latitude",
        lon="Longitude",
        hover_name="Name",
        #hovertext=["Addresses"],
        hover_data=["URL", "City","State"],
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style="mapbox://styles/hurshd0/ck86zky880ory1ip18f5tw4y6/draft",
        #mapbox_style="satellite",
        mapbox=dict(center=dict(lat=lat, lon=lon), zoom=zoom,),
        dragmode=False,
        hoverlabel={
                "bgcolor": '#900714',
                "font": {"color": 'white'},
            }
    )

    fig.data[0].update(
        #hovertemplate="<b><a href='%{customdata[0]}' style='color:#F4F4F4'>%{hovertext}</a></b>",
        #<br>Source %{customdata[0]} 
        hovertemplate="<b><a href='%{customdata[0]}' style='color:#F4F4F4'>%{hovertext}</a></b><br>%{customdata[1]},%{customdata[2]}",
        #  
        marker={"size": 15, "symbol": "marker"},
    )

    return fig
