import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import cache
from utils.settings import NCOV19_API


@cache.memoize(timeout=3600)
def confirmed_cases_chart(state=None) -> go.Figure:
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    URL = NCOV19_API + "country"
    payload = json.dumps({"alpha2Code": "US"})
    response = requests.post(URL, data=payload).json()
    data = response["message"]
    data = pd.read_json(data, orient="records")
    data = data.rename(columns={"Confirmed": "Confirmed Cases"})
    data = data.tail(60)

    fig = px.line(data, x="Date", y="Confirmed Cases")
    fig.update_traces(line_color="#F4B000")
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        template="plotly_dark",
        autosize=True,
        xaxis_title="Date",
        yaxis_title=None,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        font=dict(
            family="Roboto, sans-serif",
            size=10,
            color="#f4f4f4"
        )
    )

    return fig
