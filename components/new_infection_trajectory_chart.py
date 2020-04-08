import gc
import json
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from app import cache
from utils import REVERSE_STATES_MAP
from utils import config



# @cache.memoize(timeout=3600)
def new_infection_trajectory_chart(state="US") -> go.Figure:
    """Line chart data for the selected state.

    # TODO: Population is hardcoded we can pull it from our BE

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    if state == "US":

        URL = config.NCOV19_API + config.COUNTRY

        # US data
        payload = json.dumps({"alpha2Code": "US"})
        response = requests.post(URL, data=payload).json()
        data = response["message"]

        us = pd.DataFrame.from_records(data)
        us = us["Confirmed"].to_frame("US")

        # South Korea data
        payload = json.dumps({"alpha2Code": "KR"})
        response = requests.post(URL, data=payload).json()
        data = response["message"]
        kr = pd.DataFrame.from_records(data)
        kr = kr["Confirmed"].to_frame("South Korea")

        # Italy Data
        payload = json.dumps({"alpha2Code": "IT"})
        response = requests.post(URL, data=payload).json()
        data = response["message"]
        it = pd.DataFrame.from_records(data)
        it = it["Confirmed"].to_frame("Italy")

        # load in China, UK, and (TODO) data from JHU
        new_countries = ['China', 'United Kingdom', 'Singapore']#TODO add country]

        jhu = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/' \
            'COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'\
            'time_series_covid19_confirmed_global.csv')

        jhu = jhu[jhu['Country/Region'].isin(new_countries)]
        jhu = jhu.groupby(['Country/Region']).sum()
        jhu = jhu.T.iloc[2:]

        # scale per 100000 people
        # source: https://www.worldometers.info/world-population/population-by-country/
        CH_POP = 1439323776
        UK_POP = 67886011
        US_POP = 331002651	
        ITALY_POP = 60461826
        SK_POP = 51269185
        SI_POP = 5850342

        jhu['China'] = jhu['China'] / (CH_POP/100000)
        jhu['United Kingdom'] = jhu['United Kingdom'] / (UK_POP/100000)
        jhu['Singapore'] = jhu['Singapore'] / (SI_POP/100000)
        kr["South Korea"] = kr["South Korea"] / (SK_POP / 100000)
        us["US"] = us["US"] / (US_POP / 100000)
        it["Italy"] = it["Italy"] / (ITALY_POP / 100000)

        # filter to only after country reached 1 case per 100K people
        us = us[us["US"] > 1].reset_index(drop=True)
        kr = kr[kr["South Korea"] > 1].reset_index(drop=True)
        it = it[it["Italy"] > 1].reset_index(drop=True)
        ch = jhu[jhu['China'] > 1].reset_index(drop=True)
        uk = jhu[jhu['United Kingdom'] > 1].reset_index(drop=True)
        si = jhu[jhu['Singapore'] > 1].reset_index(drop=True)

        # merge dataframes
        merged = pd.concat([kr["South Korea"], it["Italy"], us["US"], \
            ch['China'], uk['United Kingdom'], si['Singapore']], axis=1)
        merged = merged.reset_index()
        merged = merged.rename(columns={"index": "Days"})

        # data for doubling lines

        del response, data, us, kr, it
        gc.collect()

        fig = go.Figure()

        # <extra></extra> remove name from the end of the hover over text
        template = (
            "%{y:.0f} confirmed cases per 100,000 people<br>in %{text} <extra></extra>"
        )

        countries = ["Italy", "South Korea", "Singapore", "United Kingdom", "China", "US"]
        # countries += new_countries #TODO remove when API is implemented
        colors = ["#009d00", "#009fe2", '#dbdbdb', '#dc93ff', '#ff6059', "#F4B000"]


        # Adding lines for doubling times
        max_y = merged.max().max()
        # these are y values for doubling times of [3 days, 7 days, 10 days]
        linspace = np.linspace(0,len(merged),200)
        comparison_lines = [[],[],[]]
        last_x = [len(merged)]*3
        doubling_rates = [1.2599, 1.1041, 1.0718]
        for x in linspace:
            for i, rate in enumerate(doubling_rates):
                next = 1*(rate**x)
                if next>max_y:
                    next = np.NaN
                    if last_x[i]==len(merged):
                        last_x[i] = x
                comparison_lines[i].append(next)

        for i, country in enumerate(countries):
            # CALCULATE ANNOTATION POSITION:
            annotation_x = (
                merged[["Days", country]].dropna()["Days"].max()
            )  # FIND LAST DAY ON LINE
            annotation_y = (
                merged[["Days", country]].dropna()[country].max()
            )  # FIND HIGHEST POINT ON LINE

            fig.add_trace(
                go.Scatter(
                    x=merged["Days"],
                    y=merged[country],
                    name=country,
                    line={"color": colors[i]},
                    mode="lines",
                    text=[country] * len(merged[country]),
                    hovertemplate=template,
                )
            )

            # LINE CHART ANNOTATION
            if country != 'China' and country != 'South Korea':
                fig.add_annotation(
                    x=annotation_x,
                    y=annotation_y,
                    text=country,
                    font={"size": 10},
                    xshift=1,  # Annotation x displacement!
                    yshift=7,  # Annotation y displacement!
                    showarrow=False,
                    align="left",
                    xanchor="left",
                )
            else:
                fig.add_annotation(
                    x=annotation_x,
                    y=annotation_y,
                    text=country,
                    font={"size": 10},
                    xshift=1,  # Annotation x displacement!
                    yshift=6,  # Annotation y displacement!
                    showarrow=False,
                    align="right",
                    xanchor="right",
                )

        # Add comparison lines
        annotation_texts = ['Cases double every 3 days', '...every 7 days', '...every 10 days']
        for i, line in enumerate(comparison_lines):
            # CALCULATE ANNOTATION POSITION:
            annotation_x = last_x[i]
            annotation_y = max(comparison_lines[i])

            fig.add_trace(
                go.Scatter(
                    x=linspace,
                    y=line,
                    line={"color": '#454545'},
                    mode="lines",
                    opacity = .3,
                    hoverinfo='none'
                )
            )

            x_anchor = 'center'
            if annotation_x == len(merged):
                x_anchor = 'right'

            fig.add_annotation(
                x=annotation_x,
                y=annotation_y,
                text=annotation_texts[i],
                font={"size": 7},
                xshift=3,  # Annotation x displacement!
                yshift=7,  # Annotation y displacement!
                showarrow=False,
                align="center",
                xanchor=x_anchor,
                opacity=.6
            )   

        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 1},
            template="plotly_dark",
            autosize=True,
            showlegend=False,
            legend_orientation="h",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis={"linecolor": "rgba(0,0,0,0)"},
            hoverlabel={"font": {"color": "black"}},
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
            yaxis_title="Cases per 100k People",
        )

    else:
        URL = config.NCOV19_API + config.STATE

        # State selection for comparisons

        comparison_states = ["NY", "CA", "WA"]

        states = [state]

        for s in comparison_states:
            if len(states) < 3 and s not in states:
                states.append(s)

        # Get population data
        populations = {
            "New York": 19453561,
            "Washington": 7614893,
            "California": 39512223,
        }

        state_populations = pd.read_csv("components/state-population-est2019.csv")
        state_populations = state_populations[["Region", "2019"]]
        state_populations["2019"] = state_populations["2019"].str.replace(",", "")
        state_populations["2019"] = state_populations["2019"].fillna(0)
        state_populations["2019"] = state_populations["2019"].astype(int)

        state_populations = state_populations[
            state_populations["Region"] == f".{REVERSE_STATES_MAP[state]}"
        ]

        populations[REVERSE_STATES_MAP[state]] = state_populations["2019"].iloc[0]

        # Ingestion
        series = dict()
        for i, comp_state in enumerate(states):
            payload = json.dumps({"stateAbbr": comp_state})
            response = requests.post(URL, data=payload)

            if response.status_code == 200:
                data = response.json()["message"]
                data = pd.DataFrame(data)
            else:
                backup = [
                    {"Date": "1/1/20", "Confirmed": 1337},
                    {"Date": "3/1/20", "Confirmed": 1338},
                ]
                data = pd.DataFrame(backup)
            temp_data = data["Confirmed"].to_frame(REVERSE_STATES_MAP[comp_state])
            
            # convert data to per 100K and filter where greater than 1/100K
            population = populations[REVERSE_STATES_MAP[comp_state]]
            temp_data = temp_data[
                temp_data[REVERSE_STATES_MAP[comp_state]]/(population/100000) > 1
            ].reset_index(drop=True)
            series[i] = temp_data

        merged = pd.concat([series[0], series[1], series[2]], axis=1)
        merged = merged.reset_index()
        merged = merged.rename(columns={"index": "Days"})

        del series, response
        gc.collect()

        # Get cases per 100,000 people and create state_names list
        state_names = []
        for s in states:
            name = REVERSE_STATES_MAP[s]
            state_names.append(name)
            merged[name] = merged[name] / (populations[name] / 100000)

        del state_populations, populations
        gc.collect()

        # Adding lines for doubling times
        max_y = merged.max().max()
        # these are y values for doubling times of [3 days, 7 days, 10 days]
        linspace = np.linspace(0,len(merged),200)
        comparison_lines = [[],[],[]]
        last_x = [len(merged)]*3
        doubling_rates = [1.4142, 1.2599, 1.1892]
        for x in linspace:
            for i, rate in enumerate(doubling_rates):
                next = 1*(rate**x)
                if next>max_y:
                    next = np.NaN
                    if last_x[i]==len(merged):
                        last_x[i] = x
                comparison_lines[i].append(next)


        # Plotting
        colors = ["#009fe2", "#009d00", "#F4B000"]
        fig = go.Figure()

        template = (
            "%{y:.0f} confirmed cases per 100,000 people<br>in %{text} <extra></extra>"
        )

        # reversing list so the line for input state is on top
        state_names.reverse()

        for i, name in enumerate(state_names):
            # CALCULATE ANNOTATION POSITION:
            annotation_x = (
                merged[["Days", name]].dropna()["Days"].max()
            )  # FIND LAST DAY ON LINE
            annotation_y = (
                merged[["Days", name]].dropna()[name].max()
            )  # FIND HIGHEST POINT ON LINE

            fig.add_trace(
                go.Scatter(
                    x=merged["Days"],
                    y=merged[name],
                    name=name,
                    line={"color": colors[i]},
                    mode="lines",
                    text=[name] * len(merged[name]),
                    hovertemplate=template,
                )
            )

            fig.add_annotation(
                x=annotation_x,
                y=annotation_y,
                text=name,
                font={"size": 10},
                xshift=-2,  # Annotation x displacement!
                yshift=10,  # Annotation y displacement!
                showarrow=False,
                align="right",
                xanchor="right",
            )

        # Add comparison lines
        annotation_texts = ['Cases double every 2 days', '...every 3 days', '...every 4 days']
        for i, line in enumerate(comparison_lines):
            # CALCULATE ANNOTATION POSITION:
            annotation_x = last_x[i]
            annotation_y = max(comparison_lines[i])

            fig.add_trace(
                go.Scatter(
                    x=linspace,
                    y=line,
                    line={"color": '#454545'},
                    mode="lines",
                    opacity = .3,
                    hoverinfo = 'none'
                )
            )

            x_anchor = 'center'
            if annotation_x == len(merged):
                x_anchor = 'right'

            fig.add_annotation(
                x=annotation_x,
                y=annotation_y,
                text=annotation_texts[i],
                font={"size": 7},
                xshift=3,  # Annotation x displacement!
                yshift=2,  # Annotation y displacement!
                showarrow=False,
                align="center",
                xanchor=x_anchor,
                opacity=.6
            )   


        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 1},
            template="plotly_dark",
            autosize=True,
            showlegend=False,
            legend_orientation="h",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis={"linecolor": "rgba(0,0,0,0)"},
            hoverlabel={"font": {"color": "black"}},
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
            yaxis_title="Cases per 100k People",
        )
    
    del merged
    gc.collect()

    return fig
