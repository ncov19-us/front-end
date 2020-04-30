import gc
import pandas as pd
import flask
import plotly.express as px

from ncov19_dash.utils import STATES_COORD
from ncov19_dash.components import get_all_county_data
from ncov19_dash import config
from ncov19_dash.cache import server_cache


px.set_mapbox_access_token(config.MAPBOX_ACCESS_TOKEN)


# TODO: Make Drive-thru testing center API
@server_cache.memoize(timeout=3600)
def get_drive_thru_testing_centers():
    try:
        drive_thru_df = pd.read_csv(config.DRIVE_THRU_URL)
        drive_thru_df["Street Address"] = drive_thru_df[
            "Street Address"
        ].fillna("")
    except ValueError as ex:
        print(f"[ERROR] get_drive_thru_testing_center error, {ex}")
        drive_thru_df = pd.DataFrame()

    return drive_thru_df


################################################################################
def confirmed_scatter_mapbox(state="United States"):
    """Displays choroplepth map for the data. For the whole US, the map is
    divided by state.

    :return card: A dash boostrap component Card object with a dash component
    Graph inside drawn using plotly express scatter_mapbox

    :rtype: dbc.Card
    """
    data, _ = get_all_county_data()

    color_scale = [
        "#fadc8f",
        "#f9d67a",
        "#f8d066",
        "#f8c952",
        "#f7c33d",
        "#f6bd29",
        "#f5b614",
        "#F4B000",
        "#eaa900",
        "#e0a200",
        "#dc9e00",
    ]

    # Scaled the data exponentially to show smaller values.
    data["scaled"] = data["confirmed"] ** 0.77

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
        mapbox_style=config.MAPBOX_STYLE,
        mapbox=dict(center=dict(lat=lat, lon=lon), zoom=zoom,),
    )

    fig.data[0].update(
        hovertemplate=(
            "%{customdata[3]}, %{customdata[2]}<br>Confirmed:"
            " %{customdata[0]}<br>Deaths: %{customdata[1]}"
        )
    )

    del data
    gc.collect()

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

    df = get_drive_thru_testing_centers()

    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Name",
        hover_data=["URL", "City", "State", "Street Address"],
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style=config.MAPBOX_STYLE,
        mapbox=dict(center=dict(lat=lat, lon=lon), zoom=zoom,),
        dragmode=False,
        hoverlabel={"bgcolor": "#900714", "font": {"color": "white"},},
    )

    fig.data[0].update(
        hovertemplate=(
            "<b><a href='%{customdata[0]}' style='color:#F4F4F4'>"
            "%{hovertext}</a></b><br> %{customdata[3]}<br>"
            "%{customdata[1]}, %{customdata[2]}"
        ),
        marker={"symbol": "hospital", "color": "white"},
    )

    del df
    gc.collect()

    return fig
