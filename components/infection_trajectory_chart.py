import pandas as pd

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq

from utils.settings import TIME_URL


def infection_trajectory_chart(state=None) -> dbc.Card:
    """Line chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    df = pd.read_csv(TIME_URL)
    kr = df[df["Country/Region"] == "Korea, South"]
    us = df[df["Country/Region"] == "US"]
    it = df[df["Country/Region"] == "Italy"]

    us = us[~us["Province/State"].str.contains("Princess")]
    us = us.drop(columns=["Lat", "Long", "Province/State", "Country/Region"])
    us = us.sum(axis=0).to_frame().reset_index()
    us = us.rename(columns={0: "United States"})
    us = us[us["United States"] > 200]
    us = us.reset_index(drop=True)

    it = it.drop(columns=["Lat", "Long", "Province/State", "Country/Region"])
    it = it.sum(axis=0).to_frame().reset_index()
    it = it.rename(columns={0: "Italy"})
    it = it[it["Italy"] > 200]
    it = it.reset_index(drop=True)

    kr = kr.drop(columns=["Lat", "Long", "Province/State", "Country/Region"])
    kr = kr.sum(axis=0).to_frame().reset_index()
    kr = kr.rename(columns={0: "South Korea"})
    kr = kr[kr["South Korea"] > 200]
    kr = kr.reset_index(drop=True)

    merged = pd.concat([kr["South Korea"], it["Italy"], us["United States"]], axis=1)
    merged = merged.reset_index()
    merged = merged.rename(columns={"index": "Days"})

    del df, it, kr, us

    fig = go.Figure()

    template = "%{y} confirmed cases %{x} days since 200 cases"

    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["Italy"],
            name="Italy",
            opacity=0.7,
            mode="lines+markers",
            hovertemplate=template,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["South Korea"],
            name="South Korea",
            opacity=0.7,
            mode="lines+markers",
            hovertemplate=template,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["United States"],
            name="United States",
            text="United States",
            line={"width": 5, "color": "#00BFFF"},
            mode="lines+markers",
            hovertemplate=template,
        )
    )
    fig.update_layout(
        margin={"r": 10, "t": 40, "l": 0, "b": 0},
        template="plotly_dark",
        title="Days since 200 Cases",
        showlegend=True,
    )

    card = dbc.Card(dbc.CardBody(dcc.Graph(figure=fig, style={"height": "20vh"})))
    return card
