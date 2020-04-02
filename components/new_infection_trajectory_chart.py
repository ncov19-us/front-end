import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from app import cache
from utils.settings import NCOV19_API


# @cache.memoize(timeout=3600)
def infection_trajectory_chart(state='US') -> go.Figure:
    """Line chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    if state == 'US':

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

        us = us[us["US"] > 100].reset_index(drop=True)
        kr = kr[kr["South Korea"] > 100].reset_index(drop=True)
        it = it[it["Italy"] > 100].reset_index(drop=True)

        merged = pd.concat([kr["South Korea"], it["Italy"], us["US"]], axis=1)
        merged = merged.reset_index()
        merged = merged.rename(columns={"index": "Days"})

        # scale per 100000 people
        US_POP = 329450000
        ITALY_POP = 60500000
        SK_POP = 51200000

        merged['South Korea'] = merged['South Korea']/(SK_POP/100000)
        merged['US'] = merged['US']/(US_POP/100000)
        merged['Italy'] = merged['Italy']/(ITALY_POP/100000)

        del response, data, us, kr, it

        fig = go.Figure()

        # <extra></extra> remove name from the end of the hover over text
        template = "%{y:.} confirmed cases per 100,000 people %{x} days since 100 cases<extra></extra>"

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

    else:
        # TODO uncomment
        cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
        
        # TODO remove
        # inputting data without github API
        # cases = pd.read_csv('time_series_covid19_confirmed_US.csv')

        states = set(['New York', 'Washington', 'California'])

        if state not in states:
            states.remove('Washington')
            states.add(state)

        series = dict()

        for i, comp_state in enumerate(states):
            temp = cases[cases.Province_State == comp_state]
            temp_data = pd.DataFrame(temp.aggregate('sum')[11:],columns=[comp_state])
            series[i] = temp_data[temp_data[comp_state]>100].reset_index(drop=True)
        
        series0 = series[0][series[0].columns[0]]
        series1 = series[1][series[1].columns[0]]
        series2 = series[2][series[2].columns[0]]

        merged = pd.concat([series0, series1, series2], axis=1)
        merged = merged.reset_index()
        merged = merged.rename(columns={"index": "Days"})

        # getting populations

        populations = {
            'New York':19453561,
            'Washington':7614893,
            'California':39512223
        }

        state_populations = pd.read_csv('state-population-est2019.csv')
        state_populations = state_populations[['Region', '2019']]
        state_populations['2019'] = state_populations['2019'].str.replace(',', '')
        state_populations['2019'] = state_populations['2019'].fillna(0)
        state_populations['2019'] = state_populations['2019'].astype(int)
    
        state_populations = state_populations[state_populations['Region']==f'.{state}']
        populations[state] = state_populations['2019'].iloc[0]


        # Get cases per 100,000 people
        for s in states:
            merged[s] = merged[s]/(populations[s]/100000)

        fig = go.Figure()

        # <extra></extra> remove name from the end of the hover over text
        template = "%{y:.0f} confirmed cases per 100,000 people<br>in "
        end_template = "<extra></extra>"

        fig.add_trace(
            go.Scatter(
                x=merged["Days"],
                y=merged["New York"],
                name="New York",
                # opacity=0.7,
                line={"color": "#D8B9B2"},
                mode="lines",
                hovertemplate=template+'New York'+end_template
            )
        )
        fig.add_trace(
            go.Scatter(
                x=merged["Days"],
                y=merged['California'],
                name='California',
                line={"color": "#F4B000"},
                mode="lines",
                hovertemplate=template+'California'+end_template,
            )
        )
        
        if 'Washington' not in states:
            fig.add_trace(
                go.Scatter(
                    x=merged["Days"],
                    y=merged[state],
                    name=state,
                    line={"color": "#F4B000"},
                    mode="lines",
                    hovertemplate=template+state+end_template,
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=merged["Days"],
                    y=merged["Washington"],
                    name="Washington",
                    # opacity=0.7,
                    line={"color": "#DD1E34"},
                    mode="lines",
                    hovertemplate=template+'Washington'+end_template
                ),
            )

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
