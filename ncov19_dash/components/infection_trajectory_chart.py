import gc
import plotly.graph_objects as go

from ncov19_dash.components import get_country_trajectory_data
from ncov19_dash.components import get_state_trajectory_data
from ncov19_dash.cache import server_cache


@server_cache.memoize(timeout=3600)
def infection_trajectory_chart(state="US") -> go.Figure:
    """Line chart data for the selected state.

    # TODO: Population is hardcoded we can pull it from our BE

    :params state: get the time series data for a particular state for
    confirmed, deaths, and recovered. If None, the whole US.
    """

    if state == "US":

        merged = get_country_trajectory_data()

        fig = go.Figure()

        # <extra></extra> remove name from the end of the hover over text
        template = (
            "%{y:.0f} confirmed cases per 100,000 people<br>in"
            " %{text} <extra></extra>"
        )

        countries = ["Italy", "South Korea", "US"]
        colors = ["#009d00", "#009fe2", "#F4B000"]

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
            fig.add_annotation(
                x=annotation_x,
                y=annotation_y,
                text=country,
                font={"size": 10},
                xshift=-2,  # Annotation x displacement!
                yshift=10,  # Annotation y displacement!
                showarrow=False,
                align="right",
                xanchor="right",
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
        merged, state_names = get_state_trajectory_data(state)

        # Plotting
        colors = ["#009fe2", "#009d00", "#F4B000"]
        fig = go.Figure()

        template = (
            "%{y:.0f} confirmed cases per 100,000 people<br>in"
            " %{text} <extra></extra>"
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
