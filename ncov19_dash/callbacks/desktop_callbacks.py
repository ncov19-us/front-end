from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format

from ncov19_dash.utils import STATES_COORD, REVERSE_STATES_MAP
from ncov19_dash.components import daily_stats
from ncov19_dash.components import news_feed, twitter_feed
from ncov19_dash.components import infection_trajectory_chart
from ncov19_dash.components import confirmed_scatter_mapbox
from ncov19_dash.components import drive_thru_scatter_mapbox
from ncov19_dash.components import cases_chart, deaths_chart
from ncov19_dash.components import stats_table


font_size = ".9vw"
color_active = "#F4F4F4"
color_inactive = "#AEAEAE"
color_bg = "#010914"


def register_desktop_callbacks(app):

    ############################################################################
    #
    #    Feed callbacks
    #
    ############################################################################
    @app.callback(
        Output("feed-content", "children"),
        [
            Input("left-tabs-styled-with-inline", "value"),
            Input("intermediate-value", "children"),
        ],
    )                                                   # pylint: disable=W0612
    def feed_tab_content(tab_value, state):
        """Callback to change between news and twitter feed
        """
        # print(f"feed tab value {tab_value}")
        # print(f"feed tab state {state}")
        if tab_value == "twitter-tab":
            return twitter_feed(state)

        return news_feed(state)


    @app.callback(
        Output("stats-table", "children"),
        [Input("intermediate-value", "children"),],
    )                                                   # pylint: disable=W0612
    def stats_tab_content(state):
        df = stats_table(state)

        # font_size_heading = ".4vh"
        font_size_body = ".9vw"
        table = dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[
                {"name": "State/County", "id": "State/County",},
                {
                    "name": "Confirmed",
                    "id": "Confirmed",
                    "type": "numeric",
                    "format": Format(group=","),
                },
                {
                    "name": "Deaths",
                    "id": "Deaths",
                    "type": "numeric",
                    "format": Format(group=","),
                },
            ],
            editable=False,
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            style_as_list_view=True,
            fixed_rows={"headers": True},
            fill_width=False,
            style_table={
                "width": "100%",
                "height": "100vh",
            },
            style_header={
                "backgroundColor": color_bg,
                "border": color_bg,
                "fontWeight": "bold",
                "font": "Lato, sans-serif",
                "height": "2vw",
            },
            style_cell={
                "font-size": font_size_body,
                "font-family": "Lato, sans-serif",
                "border-bottom": "0.01rem solid #313841",
                "backgroundColor": "#010915",
                "color": "#FEFEFE",
                "height": "2.75vw",
            },
            style_cell_conditional=[
                {
                    "if": {"column_id": "State/County",},
                    "minWidth": "4vw",
                    "width": "4vw",
                    "maxWidth": "4vw",
                },
                {
                    "if": {"column_id": "Confirmed",},
                    "color": "#F4B000",
                    "minWidth": "3vw",
                    "width": "3vw",
                    "maxWidth": "3vw",
                },
                {
                    "if": {"column_id": "Deaths",},
                    "color": "#E55465",
                    "minWidth": "3vw",
                    "width": "3vw",
                    "maxWidth": "3vw",
                },
            ],
        )

        return table


    @app.callback(
        Output("us-map", "figure"),
        [
            Input("middle-map-tabs-styled-with-inline", "value"),
            Input("intermediate-value", "children"),
        ],
    )                                               # pylint: disable=W0612
    def map_tab_content(value, state):
        """Callback to change between news and twitter feed
        """
        if value == "testing-us-map-tab":
            return drive_thru_scatter_mapbox(state=REVERSE_STATES_MAP[state])

        return confirmed_scatter_mapbox(state=REVERSE_STATES_MAP[state])


    ############################################################################
    #
    #    Confirm cases callback
    #
    ############################################################################
    @app.callback(
        [Output("confirmed-cases-timeline", "figure")],
        [Input("intermediate-value", "children")],
    )                                                   # pylint: disable=W0612
    def confirmed_cases_chart_callback(state):
        fig = cases_chart(state)
        return [fig]


    @app.callback(
        [Output("confirmed-cases-chart-title", "children")],
        [Input("intermediate-value", "children")],
    )                                                   # pylint: disable=W0612
    def confirmed_cases_chart_title_callback(state="US"):
        if state == "US":
            return ["U.S. Confirmed Cases"]

        return [f"{REVERSE_STATES_MAP[state]} Confirmed Cases"]


    ############################################################################
    #
    #    Deaths callback
    #
    ############################################################################
    @app.callback(
        [Output("deaths-timeline", "figure")],
        [Input("intermediate-value", "children")]
    )                                                   # pylint: disable=W0612
    def death_chart_callback(state):
        fig = deaths_chart(state)

        return [fig]


    @app.callback(
        [Output("death-chart-title", "children")],
        [Input("intermediate-value", "children")]
    )                                                   # pylint: disable=W0612
    def death_chart_title_callback(state="US"):
        if state == "US":
            return ["U.S. Deaths"]

        return [f"{REVERSE_STATES_MAP[state]} Deaths"]


    ############################################################################
    #
    #    Trajectory callback
    #
    ############################################################################
    @app.callback(
        [Output("infection-trajectory-title", "children")],
        [Input("intermediate-value", "children")],
    )                                                   # pylint: disable=W0612
    def trajectory_title_callback(state="US"):
        if state == "US":
            return ["U.S. Trajectory"]

        return [f"{REVERSE_STATES_MAP[state]} Trajectory"]


    @app.callback(
        [Output("infection-trajectory-chart", "figure")],
        [Input("intermediate-value", "children")],
    )                                                   # pylint: disable=W0612
    def trajectory_chart_callback(state):
        fig = infection_trajectory_chart(state)

        return [fig]


    ############################################################################
    #
    #    Top bar callback
    #
    ############################################################################
    @app.callback(
        [Output("daily-stats", "children")],
        [Input("intermediate-value", "children")]
    )                                                   # pylint: disable=W0612
    def daily_stats_callback(state):
        cards = daily_stats(state)

        return [cards]


    ############################################################################
    #
    #    State Dropdown Menu Callback
    #
    ############################################################################
    @app.callback(
        [Output("intermediate-value", "children")],
        [Input("states-dropdown", "value")]
    )                                                   # pylint: disable=W0612
    def update_output(state):
        state = STATES_COORD[state]["stateAbbr"]

        return [state]
