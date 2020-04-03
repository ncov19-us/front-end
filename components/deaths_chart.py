import requests
import pandas as pd
import json
import plotly.graph_objects as go
from app import cache
from utils.settings import REVERSE_STATES_MAP, NCOV19_API


@cache.memoize(timeout=3600)
def deaths_chart(state='US') -> go.Figure:
    """Bar chart data for the selected state.
    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    
    if state == 'US':
        URL = NCOV19_API + 'country'
        payload = json.dumps({"alpha2Code": "US"})
        response = requests.post(URL, data=payload).json()
        data = response["message"]
        data = pd.DataFrame(data)  # TODO remove for production
        # data = pd.read_json(data, orient="records") # TODO uncomment for production
        data = data.rename(columns={"Confirmed": "Confirmed Cases"})
        data = data.fillna(0)

    else:
        URL = NCOV19_API + 'state'
        payload = json.dumps({"stateAbbr": state})
        response = requests.post(URL, data=payload)

        if response.status_code == 200:
            data = response.json()["message"]
            data = pd.DataFrame(data)  
        else:
            backup = [{'Date': '1/1/20', 'Confirmed': 0, 'Deaths': 0},
                      {'Date': '3/1/20', 'Confirmed': 0, 'Deaths': 0}]
            data = pd.DataFrame(backup)

        data = data.rename(columns={"Confirmed": "Confirmed Cases"})
        
    # Calculate new cases and death for each day
    data["New Confirmed Cases"] = data["Confirmed Cases"].diff()
    data["New Deaths"] = data["Deaths"].diff()

    # Turn date into datetime format
    data['Date'] = pd.to_datetime(data['Date'], infer_datetime_format=False)

    data = data.tail(30)
    # Limit data to 1% of current maximum number of cases
    #     data = data[data['Confirmed Cases'] > data['Confirmed Cases'].max() * 0.01]

    # Calculate annotation placements
    plot_tail = data.iloc[-1].to_list()
    annotation_x = plot_tail[0]  # LAST TIMESTAMP
    annotation_y1 = plot_tail[2]  # LAST DEATHS COUNT
    annotation_y2 = data['New Deaths'].max()  # HIGHEST BAR ON BAR CHART

    template_new = "%{y} confirmed new deaths on %{x}<extra></extra>"
    template_total = "%{y} confirmed total deaths on %{x}<extra></extra>"
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data["Date"],
            y=data["New Deaths"],
            name="New Deaths",
            marker={"color": "#870000"},
            hovertemplate=template_new,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Deaths"],
            name="Total Deaths",
            line={"color": "#870000"},
            mode="lines",
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
        showarrow=False
    )

    # BAR CHART ANNOTATION
    fig.add_annotation(
        x=annotation_x,
        y=annotation_y2,
        text="Daily New Deaths",
        font={"size": 10},
        xshift=-40,  # Annotation x displacement!
        yshift=10,  # Annotation y displacement!
        showarrow=False
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
        font=dict(
            family="Roboto, sans-serif",
            size=10,
            color="#f4f4f4"
        ),
        yaxis_title="Number of deaths",
        # xaxis_title="Date"
        #         legend=dict(
        #                 title=None, orientation="h", y=-.5, yanchor="bottom", x=0, xanchor="left"
        #         )
    )

    return fig
