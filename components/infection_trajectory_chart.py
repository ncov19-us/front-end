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

    if state == 'US':

        # TODO adjust for population

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

        US_POP = 329450000
        ITALY_POP = 60500000
        SK_POP = 51200000

        merged['South Korea'] = merged['South Korea']/(SK_POP/100000)
        merged['US'] = merged['US']/(US_POP/100000)
        merged['Italy'] = merged['Italy']/(ITALY_POP/100000)

        # TODO scale for population

        del response, data, us, kr, it

        fig = go.Figure()

        # <extra></extra> remove name from the end of the hover over text
        template = "%{y} confirmed cases per 100,000 people %{x} days since 200 cases<extra></extra>"

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
        # codes = pd.read_csv('state-codes.csv')
        cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')



        # temp #TODO REMOVE
        # FAKE_DATA = [1,2,3,4,5,150,160,170]

        # FAKE_DATES = []
        # for i in range(len(FAKE_DATA)):
        #     FAKE_DATES.append(f'3/{i+1}/19')

        # FAKE_CASES = pd.DataFrame({'Date': FAKE_DATES, 'Cases':FAKE_DATA})




        # get confirmed cases df
        state_data = cases[cases.Province_State == state]
        data = pd.DataFrame(state_data.aggregate('sum')[11:],columns=[state])
        
        # filter to only see past 120 confirmed cases
        data = data[data[state]>=120]

        comparison_states = ['New York', 'Washington']

        for comp_state in comparison_states:
            temp = cases[cases.Province_State == comp_state]
            temp_data = pd.DataFrame(temp.aggregate('sum')[11:],columns=[comp_state])
            temp_data = temp_data[temp_data[comp_state]>=120]
            data[comp_state] = temp_data[comp_state]

        state_populations = pd.read_csv('state-population-est2019.csv')
        state_populations = state_populations[['Region', '2019']]
        state_populations['2019'] = state_populations['2019'].str.replace(',', '')
        state_populations['2019'] = state_populations['2019'].fillna(0)
        state_populations['2019'] = state_populations['2019'].astype(int)
    
        # df.iloc[:,:].str.replace(',', '').astype(float)
        state_populations = state_populations[state_populations['Region']==f'.{state}']
        state_population = state_populations['2019'].iloc[0]
        NY_POP = 19453561
        WA_POP = 7614893

        # Get cases per 100,000 people

        data[state] = data[state]/(state_population/100000)
        if state != 'New York':
            data['New York'] = data['New York']/(NY_POP/100000)
        if state != 'Washington':
            data['Washington'] = data['Washington']/(WA_POP/100000)

        data['Date'] = data.index

        merged = data.iloc[39:]

        fig = go.Figure()

        # <extra></extra> remove name from the end of the hover over text
        template = "%{y} confirmed cases per 100,000 people %{x} days after 120 confirmed cases in "
        end_template = "<extra></extra>"

        fig.add_trace(
            go.Scatter(
                x=merged["Date"],
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
                x=merged["Date"],
                y=merged["Washington"],
                name="Washington",
                # opacity=0.7,
                line={"color": "#DD1E34"},
                mode="lines",
                hovertemplate=template+'Washington'+end_template
            ),
        )
        if state not in comparison_states:
            fig.add_trace(
                go.Scatter(
                    x=merged["Date"],
                    y=merged[state],
                    name=state,
                    line={"color": "#F4B000"},
                    mode="lines",
                    hovertemplate=template+state+end_template,
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

    return fig
