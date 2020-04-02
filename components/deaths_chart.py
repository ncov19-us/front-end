import requests
import pandas as pd
import json
import plotly.graph_objects as go
from utils.settings import REVERSE_STATES_MAP


# @cache.memoize(timeout=3600)
def deaths_chart(state='US') -> go.Figure:
    """Bar chart data for the selected state.
    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    root = 'https://covid19-us-api-staging.herokuapp.com/'  # TODO change for production
    if state == 'US':
        URL = root + 'country'
        payload = json.dumps({"alpha2Code": "US"})
        # staging API
        URL = 'https://covid19-us-api-staging.herokuapp.com/' + "country"
        # production API
        # URL = "https://covid19-us-api.herokuapp.com/" + "country"
        response = requests.post(URL, data=payload).json()
        data = response["message"]
        data = pd.DataFrame(data)  # TODO remove for production
        # data = pd.read_json(data, orient="records") # TODO uncomment for production
        data = data.rename(columns={"Confirmed": "Confirmed Cases"})
        data = data.fillna(0)

    else:
        # TODO need to get from db when data is available
        # URL = root + 'stats'
        # payload = json.dumps({'state': state})
        # TODO add error handling, try except
        ##########################################
        # Section for reading data from csv file #
        ##########################################
        # Read CSV data from JHU github repo:
        cases = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
        deaths = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

        state = REVERSE_STATES_MAP[state]
        # get confirmed cases df
        data = cases[cases["Province_State"] == state]
        data = pd.DataFrame(data.aggregate('sum')[11:], columns=['Confirmed Cases'])
        # get death data
        deaths = deaths[deaths.Province_State == state]
        deaths = deaths.aggregate('sum')[12:]
        # combine
        data['Deaths'] = deaths
        data = data.reset_index()
        data.columns = ['Date', 'Confirmed Cases', 'Deaths']
        data = data.fillna(0)
        ###########################################
        #               end section               #
        ###########################################

    # Calculate new cases and death for each day
    data["New Confirmed Cases"] = data["Confirmed Cases"].diff()
    data["New Deaths"] = data["Deaths"].diff()

    # Turn date into datetime format
    data['Date'] = pd.to_datetime(data['Date'], infer_datetime_format=False)

    data = data.tail(30)
    # Limit data to 1% of current maximum number of cases
    #     data = data[data['Confirmed Cases'] > data['Confirmed Cases'].max() * 0.01]

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
