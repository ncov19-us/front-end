from datetime import datetime, timedelta
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from app import cache

from utils.settings import BASE_URL, MAPBOX_ACCESS_TOKEN

px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

# Data comes from JHU CSSE Github Repo, will be moved to more proper API
# TODO: Remove logic from here and give it to API endpoint
def wrangle_daily_reports(df: pd.DataFrame) -> pd.DataFrame:
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


# TODO: Remove logic from here and give it to API endpoint
def get_daily_reports() -> pd.DataFrame:
    try:
        todays_date = datetime.now().strftime("%m-%d-%Y")
        csv_url = BASE_URL + todays_date + ".csv"
        daily_reports = pd.read_csv(csv_url)
    except Exception as ex:
        previous_day_date = datetime.now() - timedelta(days=1)
        previous_day_date = previous_day_date.strftime("%m-%d-%Y")
        csv_url = BASE_URL + previous_day_date + ".csv"
        daily_reports = pd.read_csv(csv_url)
    daily_reports = wrangle_daily_reports(daily_reports)
    return daily_reports


# TODO: Make Drive-thru testing center API
def get_drive_thru_testing_centers():
    try:
        drive_thru_df = pd.read_csv(
            "https://raw.githubusercontent.com/ncov19-us/ds/master/drive_thru_testing_locations/us-drive-thru-testing-locations.csv"
        )
    except Exception as ex:
        print(ex)
    return drive_thru_df


########################################################################
#
# App Callbacks
#
########################################################################

# @app.callback(Output("us-map", "figure"), [Input("map-input", "value")])
@cache.memoize(timeout=3600)
def confirmed_scatter_mapbox():
    """Displays choroplepth map for the data. For the whole US, the map is divided by state.
    TODO: For individual states,the map will be divided by county lines. Add callbacks

    :return card: A dash boostrap component Card object with a dash component Graph inside drawn using plotly express scatter_mapbox
    :rtype: dbc.Card
    """
    color_scale = ["#ffbaba", "#ff7b7b", "#ff5252", "#ff0000", "#a70000"]
    fig = px.scatter_mapbox(
        get_daily_reports(),
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
        # Title still no show after this
        title="Corona Virus Cases in U.S.",
        title_x=0.1,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # This takes away the colorbar on the right hand side of the plot
        coloraxis_showscale=False,
        mapbox_style="dark",
        mapbox=dict(
            center=dict(lat=39.8097343, lon=-98.5556199),
            zoom=2.3),
    )

    # https://community.plot.ly/t/plotly-express-scatter-mapbox-hide-legend/36306/2
    # print(fig.data[0].hovertemplate)
    # <b>%{hovertext}</b><br><br>Confirmed=%{marker.color}\\
    # <br>Deaths=%{customdata[1]}<br>Recovered=%{customdata[2]}<br>Latitude=%{lat}<br>Longitude=%{lon}
    fig.data[0].update(
        hovertemplate="%{customdata[3]}<br>Confirmed: %{marker.size}<br>Deaths: %{customdata[1]}<br>Recovered: %{customdata[2]}"
    )

    # card = dbc.Card(dbc.CardBody(dcc.Graph(figure=fig, style={"height": "54vh"})))
    # return card
    return fig


def drive_thru_scatter_mapbox():
    fig = px.scatter_mapbox(
        get_drive_thru_testing_centers(),
        lat="Latitude",
        lon="Longitude",
        hover_name="Name",
        hover_data=["URL"],
    )
    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style="dark",
        mapbox=dict(center=dict(lat=39.8097343, lon=-98.5556199), zoom=3),
    )
    # print(fig.data[0].hovertemplate)
    fig.data[0].update(
        hovertemplate="<b><a href='%{customdata[0]}' style='color:white'>%{hovertext}</a></b>",
        marker={"size": 10, "symbol": "marker"},
    )

    return fig
