import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import cache
from utils.settings import TIME_URL


# @cache.memoize(timeout=3600)
def confirmed_cases_chart(state=None) -> go.Figure:
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    df = pd.read_csv(TIME_URL)
    df = df[df["Country/Region"] == "US"]
    # "Let it go, let it go" - Princess Elsa
    df = df[~df["Province/State"].str.contains("Princess")]
    df = df.drop(columns=["Lat", "Long", "Province/State", "Country/Region"])
    df = df.sum(axis=0).to_frame().reset_index()
    df["index"] = pd.to_datetime(df["index"])
    df = df.rename(columns={"index": "Date", 0: "Confirmed Cases"})
    df = df[30:]

    fig = px.line(df, x="Date", y="Confirmed Cases")
    fig.update_traces(line_color="#FEC400")
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        template="plotly_dark",
        # title="U.S. Confirmed Cases",
        autosize=True,
        xaxis_title="Confirmed Cases",
        yaxis_title=None,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )
    # print(fig)
    # card = dbc.Card(dbc.CardBody(dcc.Graph(figure=fig, style={"height": "20vh"})))
    # return card
    return fig
