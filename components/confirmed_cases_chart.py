import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import cache
from utils import config


@cache.memoize(timeout=3600)
def confirmed_cases_chart(state=None) -> go.Figure:
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    URL = config.NCOV19_API + config.COUNTRY
    payload = json.dumps({"alpha2Code": "US"})
    response = requests.post(URL, data=payload).json()
    data = response["message"]
    data = pd.DataFrame.from_records(data)
    data = data.rename(columns={"Confirmed": "Confirmed Cases"})
    data = data.tail(60)

    template_cases = "%{y} confirmed cases on %{x}<extra></extra>"
    template_deaths = "%{y} confirmed deaths on %{x}<extra></extra>"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Confirmed Cases"],
            name="Confirmed Cases",
            line={"color": "#F4B000"},
            mode="lines",
            hovertemplate=template_cases,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Deaths"],
            name="Deaths",
            line={"color": "#870000"},
            mode="lines",
            hovertemplate=template_deaths,
        ),
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 1},
        template="plotly_dark",
        # annotations=annotations,
        autosize=True,
        showlegend=True,
        legend_orientation="h",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # xaxis_title="Number of Days",
        yaxis={"linecolor": "rgba(0,0,0,0)"},
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={"tickformat": "%m/%y"},
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        legend=dict(
            title=None, orientation="h", y=-0.5, yanchor="bottom", x=0, xanchor="left"
        ),
    )

    return fig
