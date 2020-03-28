from datetime import datetime, timedelta
import pandas as pd
import flask
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

from app import cache
from utils.settings import MAPBOX_ACCESS_TOKEN, DRIVE_THRU_URL, NCOV19_API, MAPBOX_STYLE
import requests


DRIVE_THRU_URL = "https://raw.githubusercontent.com/ncov19-us/ds/master/drive_thru_testing_locations/us-drive-thru-testing-locations.csv"
states_lat_long = [
    {"state": "Alabama", "latitude": 32.806671, "longitude": -86.791130},
    {"state": "Alaska", "latitude": 61.370716, "longitude": -152.404419},
    {"state": "Arizona", "latitude": 33.729759, "longitude": -111.431221},
    {"state": "Arkansas", "latitude": 34.969704, "longitude": -92.373123},
    {"state": "California", "latitude": 36.116203, "longitude": -119.681564},
    {"state": "Colorado", "latitude": 39.059811, "longitude": -105.311104},
    {"state": "Connecticut", "latitude": 41.597782, "longitude": -72.755371},
    {"state": "Delaware", "latitude": 39.318523, "longitude": -75.507141},
    {"state": "District of Columbia", "latitude": 38.897438, "longitude": -77.026817},
    {"state": "Florida", "latitude": 27.766279, "longitude": -81.686783},
    {"state": "Georgia", "latitude": 33.040619, "longitude": -83.643074},
    {"state": "Hawaii", "latitude": 21.094318, "longitude": -157.498337},
    {"state": "Idaho", "latitude": 44.240459, "longitude": -114.478828},
    {"state": "Illinois", "latitude": 40.349457, "longitude": -88.986137},
    {"state": "Indiana", "latitude": 39.849426, "longitude": -86.258278},
    {"state": "Iowa", "latitude": 42.011539, "longitude": -93.210526},
    {"state": "Kansas", "latitude": 38.526600, "longitude": -96.726486},
    {"state": "Kentucky", "latitude": 37.668140, "longitude": -84.670067},
    {"state": "Louisiana", "latitude": 31.169546, "longitude": -91.867805},
    {"state": "Maine", "latitude": 44.693947, "longitude": -69.381927},
    {"state": "Maryland", "latitude": 39.063946, "longitude": -76.802101},
    {"state": "Massachusetts", "latitude": 42.230171, "longitude": -71.530106},
    {"state": "Michigan", "latitude": 43.326618, "longitude": -84.536095},
    {"state": "Minnesota", "latitude": 45.694454, "longitude": -93.900192},
    {"state": "Mississippi", "latitude": 32.741646, "longitude": -89.678696},
    {"state": "Missouri", "latitude": 38.456085, "longitude": -92.288368},
    {"state": "Montana", "latitude": 46.921925, "longitude": -110.454353},
    {"state": "Nebraska", "latitude": 41.125370, "longitude": -98.268082},
    {"state": "Nevada", "latitude": 38.313515, "longitude": -117.055374},
    {"state": "New Hampshire", "latitude": 43.452492, "longitude": -71.563896},
    {"state": "New Jersey", "latitude": 40.298904, "longitude": -74.521011},
    {"state": "New Mexico", "latitude": 34.840515, "longitude": -106.248482},
    {"state": "New York", "latitude": 42.165726, "longitude": -74.948051},
    {"state": "North Carolina", "latitude": 35.630066, "longitude": -79.806419},
    {"state": "North Dakota", "latitude": 47.528912, "longitude": -99.784012},
    {"state": "Ohio", "latitude": 40.388783, "longitude": -82.764915},
    {"state": "Oklahoma", "latitude": 35.565342, "longitude": -96.928917},
    {"state": "Oregon", "latitude": 44.572021, "longitude": -122.070938},
    {"state": "Pennsylvania", "latitude": 40.590752, "longitude": -77.209755},
    {"state": "Rhode Island", "latitude": 41.680893, "longitude": -71.511780},
    {"state": "South Carolina", "latitude": 33.856892, "longitude": -80.945007},
    {"state": "South Dakota", "latitude": 44.299782, "longitude": -99.438828},
    {"state": "Tennessee", "latitude": 35.747845, "longitude": -86.692345},
    {"state": "Texas", "latitude": 31.054487, "longitude": -97.563461},
    {"state": "Utah", "latitude": 40.150032, "longitude": -111.862434},
    {"state": "Vermont", "latitude": 44.045876, "longitude": -72.710686},
    {"state": "Virginia", "latitude": 37.769337, "longitude": -78.169968},
    {"state": "Washington", "latitude": 47.400902, "longitude": -121.490494},
    {"state": "West Virginia", "latitude": 38.491226, "longitude": -80.954453},
    {"state": "Wisconsin", "latitude": 44.268543, "longitude": -89.616508},
    {"state": "Wyoming", "latitude": 42.755966, "longitude": -107.302490},
]
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

def confirmed_scatter_mapbox(state=None):
    """Displays choroplepth map for the data. For the whole US, the map is divided by state.
    TODO: For individual states,the map will be divided by county lines. Add callbacks

    :return card: A dash boostrap component Card object with a dash component Graph inside drawn using plotly express scatter_mapbox
    :rtype: dbc.Card
    """
    URL = NCOV19_API + "county"
    response = requests.get(URL).json()
    data = response['message']
    data = pd.read_json(data, orient='records')
    data['State Name'] = data['State Name'].str.title()
    data['County Name'] = data['County Name'].str.title()


    color_scale = [ '#FA9090', '#F77A7A', '#F56666',
                    '#F15454', '#ED4343', '#E93535', '#E42828', '#DE1E1E', '#D71515', '#CF0D0D',
                    '#C70707', '#BD0202', '#B30000', '#A90000', '#9E0000', '#920000', '#870000']


    # set lat/long
    if not state:
        lat, lon = 39.8097343, -98.5556199
    elif state == "New York":
        lat, lon = 43.2994, -74.2179
    else:
        lat, lon = 39.8097343, -98.5556199

    fig = px.scatter_mapbox(
        data,
        lat="Latitude",
        lon="Longitude",
        color="Confirmed",
        size="Confirmed",
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
        mapbox=dict(center=dict(lat=lat, lon=lon),
                                zoom=flask.session['zoom']),
    )

    # https://community.plot.ly/t/plotly-express-scatter-mapbox-hide-legend/36306/2
    # print(fig.data[0].hovertemplate)
    fig.data[0].update(
        hovertemplate="%{customdata[3]}, %{customdata[2]}<br>Confirmed: %{marker.size}<br>Deaths: %{customdata[1]}"
    )

    return fig


def drive_thru_scatter_mapbox():
    """DO NOT CACHE. NEED APP_STATE TO CHANGE DYNAMICALLY
    """
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
        mapbox=dict(center=dict(lat=39.8097343, lon=-98.5556199),
                    zoom=flask.session['zoom']),
        dragmode=False,
    )

    fig.data[0].update(
        hovertemplate="<b><a href='%{customdata[0]}' style='color:black'>%{hovertext}</a></b>",
        marker={"size": 10, "symbol": "marker"},
    )

    return fig
