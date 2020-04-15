import gc
import json
import requests
import pandas as pd
import plotly.graph_objects as go
from ncov19_dash.flask_server import cache
from ncov19_dash.utils import REVERSE_STATES_MAP
from ncov19_dash.utils import config


def human_format(num):
    """
    Formats a number and returns a human-readable version of it in string form. Ex: 300,000 -> 300k
    :params num: number to be converted to a formatted string
    """
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(num).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )


@cache.memoize(timeout=3600)
def deaths_chart(state="US") -> go.Figure:
    """Bar chart data for the selected state.
    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    if state == "US":
        URL = config.NCOV19_API + config.COUNTRY
        payload = json.dumps({"alpha2Code": "US"})
        response = requests.post(URL, data=payload).json()
        data = response["message"]
        data = pd.DataFrame(data)
        data = data.rename(columns={"Confirmed": "Confirmed Cases"})
        data = data.fillna(0)

    else:
        URL = config.NCOV19_API + config.STATE
        payload = json.dumps({"stateAbbr": state})
        response = requests.post(URL, data=payload)

        if response.status_code == 200:
            data = response.json()["message"]
            data = pd.DataFrame(data)
        else:
            backup = [
                {"Date": "1/1/20", "Confirmed": 0, "Deaths": 0},
                {"Date": "3/1/20", "Confirmed": 0, "Deaths": 0},
            ]
            data = pd.DataFrame(backup)

        data = data.rename(columns={"Confirmed": "Confirmed Cases"})

    del payload, response
    gc.collect()

    # Calculate new cases and death for each day
    data["New Confirmed Cases"] = data["Confirmed Cases"].diff()
    data["New Deaths"] = data["Deaths"].diff()

    # Turn date into datetime format
    data["Date"] = pd.to_datetime(data["Date"], infer_datetime_format=False)

    data = data.tail(30)
    # Limit data to 1% of current maximum number of cases
    #     data = data[data['Confirmed Cases'] > data['Confirmed Cases'].max() * 0.01]

    # Calculate annotation placements
    plot_tail = data.iloc[-1].to_list()
    annotation_x = plot_tail[0]  # LAST TIMESTAMP
    annotation_y1 = plot_tail[2]  # LAST DEATHS COUNT
    annotation_y2 = data["New Deaths"].max()  # HIGHEST BAR ON BAR CHART

    template_new = "%{customdata} new deaths on %{x}<extra></extra>"
    template_total = "%{customdata} total deaths on %{x}<extra></extra>"
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data["Date"],
            y=data["New Deaths"],
            name="New Deaths",
            marker={"color": "#dd1e34"},
            customdata=[human_format(x) for x in data["New Deaths"].to_list()],
            hovertemplate=template_new,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Deaths"],
            name="Total Deaths",
            line={"color": "#dd1e34"},
            mode="lines",
            customdata=[human_format(x) for x in data["Deaths"].to_list()],
            hovertemplate=template_total,
        )
    )

    # LINE CHART ANNOTATION
    fig.add_annotation(
        x=annotation_x,
        y=annotation_y1,
        text="Total COVID-19 Deaths",
        font={"size": 10},
        xshift=-65,  # Annotation x displacement!
        showarrow=False,
    )

    # BAR CHART ANNOTATION
    fig.add_annotation(
        x=annotation_x,
        y=annotation_y2,
        text="Daily New Deaths",
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
        plot_bgcolor="rgba(0,0,0,0)",
        # xaxis_title="Number of Days",
        yaxis={"linecolor": "rgba(0,0,0,0)"},
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={"tickformat": "%m/%d"},
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        yaxis_title="Number of deaths",
        # xaxis_title="Date"
        #         legend=dict(
        #                 title=None, orientation="h", y=-.5, yanchor="bottom", x=0, xanchor="left"
        #         )
    )

    del data
    gc.collect()
    
    return fig
