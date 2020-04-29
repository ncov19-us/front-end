import gc
import pandas as pd

import plotly.graph_objects as go

from ncov19_dash.cache import server_cache
from ncov19_dash import config
from ncov19_dash.components import get_country_timeseries
from ncov19_dash.components import get_state_timeseries
from ncov19_dash.components import human_format


@server_cache.memoize(timeout=3600)
def cases_chart(state="US") -> go.Figure:
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for
    confirmed, deaths, and recovered. If None, the whole US.
    """

    if state == "US":
        data = get_country_timeseries(alpha2code=state)
    else:
        data = get_state_timeseries(state=state)

    # Calculate new cases and death for each day
    data["New Confirmed Cases"] = data["Confirmed Cases"].diff()
    data["New Deaths"] = data["Deaths"].diff()

    # Turn date into datetime format
    data["Date"] = pd.to_datetime(data["Date"], infer_datetime_format=False)

    data = data.tail(30)
    # Limit data to 1% of current maximum number of cases
    #data = data[data['Confirmed Cases'] > data['Confirmed Cases'].max() * 0.01]

    # Calculate annotation placements
    plot_tail = data.iloc[-1].to_list()
    annotation_x = plot_tail[0]  # LAST TIMESTAMP
    annotation_y1 = plot_tail[1]  # LAST CONFIRMED CASES COUNT
    annotation_y2 = data["New Confirmed Cases"].max()# HIGHEST BAR ON BAR CHART

    template_new = "%{customdata} new cases on %{x}<extra></extra>"
    template_total = "%{customdata} total cases on %{x}<extra></extra>"
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data["Date"],
            y=data["New Confirmed Cases"],
            name="New Cases Added",
            marker={"color": "#F4B000"},
            customdata=[human_format(x) for x in \
                data["New Confirmed Cases"].to_list()],
            hovertemplate=template_new,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Confirmed Cases"],
            name="Total Confirmed Cases",
            line={"color": "#F4B000"},
            mode="lines",
            customdata=[human_format(x) for x in \
                data["Confirmed Cases"].to_list()],
            hovertemplate=template_total,
        )
    )

    # LINE CHART ANNOTATION
    fig.add_annotation(
        x=annotation_x,
        y=annotation_y1,
        text="Total COVID-19 Cases",
        font={"size": 10},
        xshift=-65,  # Annotation x displacement!
        showarrow=False,
    )

    # BAR CHART ANNOTATION
    fig.add_annotation(
        x=annotation_x,
        y=annotation_y2,
        text="Daily New Cases",
        font={"size": 10},
        xshift=-40,  # Annotation x displacement!
        yshift=10,  # Annotation y displacement!
        showarrow=False,
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 1},
        template="plotly_dark",
        # annotations=annotations,
        autosize=True,
        showlegend=False,
        legend_orientation="h",
        paper_bgcolor="rgba(0,0,0,0)",
        #         paper_bgcolor="black",
        plot_bgcolor="rgba(0,0,0,0)",
        #         plot_bgcolor="black",
        # xaxis_title="Number of Days",
        yaxis={"linecolor": "rgba(0,0,0,0)"},
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={"tickformat": "%m/%d"},
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        yaxis_title="Number of cases",
    )

    del data
    gc.collect()

    return fig
