import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from app import cache
from utils.settings import NCOV19_API



# @cache.memoize(timeout=3600)
def infection_trajectory_chart(state=None) -> go.Figure:
    """Line chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    URL = NCOV19_API + "country"
    response = requests.get(URL).json()
    data = response['message']
    data = pd.read_json(data, orient='records')
    
    us = data["US"].to_frame("US")
    kr = data["South Korea"].to_frame("South Korea")
    it = data["Italy"].to_frame("Italy")

    us = us[us["US"] > 200].reset_index(drop=True)
    kr = kr[kr["South Korea"] > 200].reset_index(drop=True)
    it = it[it["Italy"] > 200].reset_index(drop=True)

    merged = pd.concat([kr["South Korea"], it["Italy"], us["US"]], axis=1)
    merged = merged.reset_index()
    merged = merged.rename(columns={"index": "Days"})

    fig = go.Figure()

    template = "%{y} confirmed cases %{x} days since 200 cases"

    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["Italy"],
            name="Italy",
            # opacity=0.7,
            line={"color": "#D92C25"},
            mode="lines",
            hovertemplate=template,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["South Korea"],
            name="South Korea",
            # opacity=0.7,
            line={"color": "#03DA32"},
            mode="lines",
            hovertemplate=template,
        ),

    )
    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["US"],
            name="United States",
            text="United States",
            line={"width": 5, "color": "#FEC400"},
            mode="lines",
            hovertemplate=template,
        )
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        template="plotly_dark",
        # title="Days since 200 Cases",
        autosize=True,
        showlegend=True,
        legend_orientation="h",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_showgrid=False,
        hoverlabel={"font": {"color": "black"}},
    )

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    return fig
