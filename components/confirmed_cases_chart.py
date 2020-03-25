import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import cache
from utils.settings import NCOV19_API
import requests


# @cache.memoize(timeout=3600)
def confirmed_cases_chart(state=None) -> go.Figure:
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    URL = NCOV19_API + "country"
    response = requests.get(URL).json()
    data = response['message']
    data = pd.read_json(data, orient='records')
    data = data[["US"]]
    

    data = data.rename(columns={"US":"Confirmed Cases"})
    data.index.names = ['Date']
    data = data.reset_index()
    
    fig = px.line(data, x="Date", y="Confirmed Cases")
    fig.update_traces(line_color="#FEC400")
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        template="plotly_dark",
        # title="U.S. Confirmed Cases",
        autosize=True,
        xaxis_title="Confirmed Cases",
        yaxis_title=None,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )
    
    return fig
