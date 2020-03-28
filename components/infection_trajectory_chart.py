import pandas as pd
import requests
import json
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

    # US data
    payload = json.dumps({"alpha2Code": "US"})
    response = requests.post(URL, data=payload).json()
    data = response["message"]
    us = pd.read_json(data, orient="records")
    us = us["Confirmed"].to_frame("US")

    # South Korea data
    payload = json.dumps({"alpha2Code": "KR"})
    response = requests.post(URL, data=payload).json()
    data = response["message"]
    kr = pd.read_json(data, orient="records")
    kr = kr["Confirmed"].to_frame("South Korea")

    # Italy Data
    payload = json.dumps({"alpha2Code": "IT"})
    response = requests.post(URL, data=payload).json()
    data = response["message"]
    it = pd.read_json(data, orient="records")
    it = it["Confirmed"].to_frame("Italy")

    us = us[us["US"] > 200].reset_index(drop=True)
    kr = kr[kr["South Korea"] > 200].reset_index(drop=True)
    it = it[it["Italy"] > 200].reset_index(drop=True)

    merged = pd.concat([kr["South Korea"], it["Italy"], us["US"]], axis=1)
    merged = merged.reset_index()
    merged = merged.rename(columns={"index": "Days"})

    fig = go.Figure()

    # <extra></extra> remove name from the end of the hover over text
    template = "%{y} confirmed cases %{x} days since 200 cases<extra></extra>"

    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["Italy"],
            name="Italy",
            # opacity=0.7,
            line={"color": "#D8B9B2"},
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
            line={"color": "#DD1E34"},
            mode="lines",
            hovertemplate=template,
        ),
    )
    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["US"],
            name="United States",
            line={"color": "#F4B000"},
            mode="lines",
            hovertemplate=template,
        )
    )
    # print(merged["US"].dropna().tail(1).index[0])
    # print(merged["US"].dropna().tail(1))
    
    # annotations = []
    # annotations.append(dict(xref='paper',
    #                         x=pd.to_numeric(merged["US"].dropna().tail(1).index[0]),
    #                         y=merged["US"].dropna().tail(1),
    #                         xanchor='right', yanchor='middle',
    #                         text="United States",#label + ' {}%'.format(y_trace[0]),
    #                         font=dict(family='Arial',
    #                                  size=12),
    #                         showarrow=False))
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
        font=dict(
            family="Roboto, sans-serif",
            size=10,
            color="#f4f4f4"
        ),
        # legend=dict(
        #         title=None, orientation="v", y=-.35, yanchor="bottom", x=.5, xanchor="center"
        # )
    )

    return fig
