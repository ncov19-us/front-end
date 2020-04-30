from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format

from ncov19_dash.utils import STATES_COORD, REVERSE_STATES_MAP
from ncov19_dash.components import daily_stats_mobile
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


def register_mobile_callbacks(app):

    ############################################################################
    #
    #    Confirm cases chart callback
    #
    ############################################################################
    @app.callback(
        [Output("mobile-confirmed-cases-timeline", "figure")],
        [Input("mobile-intermediate-value", "children")],
    )  # pylint: disable=W0612
    def mobile_confirmed_cases_chart_callback(state="US"):
        fig = cases_chart(state)

        return [fig]

    @app.callback(
        [Output("mobile-confirmed-cases-chart-title", "children")],
        [Input("mobile-intermediate-value", "children")],
    )  # pylint: disable=W0612
    def mobile_confirmed_cases_chart_title_callback(state="US"):
        if state == "US":
            return ["U.S. Confirmed Cases"]

        return [f"{REVERSE_STATES_MAP[state]} Confirmed Cases"]

    ############################################################################
    #
    #    Deaths chart callback
    #
    ############################################################################
    @app.callback(
        [Output("mobile-deaths-chart-title", "children")],
        [Input("mobile-intermediate-value", "children")],
    )  # pylint: disable=W0612
    def mobile_death_chart_callback(state="US"):
        if state == "US":
            return ["U.S. Deaths"]

        return [f"{REVERSE_STATES_MAP[state]} Deaths"]

    @app.callback(
        [Output("mobile-deaths-timeline", "figure")],
        [Input("mobile-intermediate-value", "children")],
    )  # pylint: disable=W0612
    def mobile_death_chart_title_callback(state):
        fig = deaths_chart(state)

        return [fig]

    ############################################################################
    #
    #    Trajectory callback
    #
    ############################################################################
    @app.callback(
        [Output("mobile-trajectory-chart", "figure")],
        [Input("mobile-intermediate-value", "children")],
    )  # pylint: disable=W0612
    def mobile_trajectory_chart_callback(state):
        fig = infection_trajectory_chart(state)

        return [fig]

    @app.callback(
        [Output("mobile-trajectory-title", "children")],
        [Input("mobile-intermediate-value", "children")],
    )  # pylint: disable=W0612
    def mobile_trajectory_title_callback(state="US"):
        if state == "US":
            return ["U.S. Trajectory"]

        return [f"{REVERSE_STATES_MAP[state]} Trajectory"]

    ############################################################################
    #
    #    Top bar callback
    #
    ############################################################################
    @app.callback(
        [Output("mobile-daily-stats", "children")],
        [Input("mobile-intermediate-value", "children")],
    )  # pylint: disable=W0612
    def daily_stats_mobile_callback(state):
        cards = daily_stats_mobile(state)

        return [cards]

    ############################################################################
    #
    #    State Dropdown Menu Callback
    #
    ############################################################################
    @app.callback(
        [Output("mobile-intermediate-value", "children")],
        [Input("mobile-states-dropdown", "value")],
    )  # pylint: disable=W0612
    def update_output(state):
        state = STATES_COORD[state]["stateAbbr"]

        return [state]

    @app.callback(
        Output("mobile-stats-table", "children"),
        [Input("mobile-intermediate-value", "children"),],
    )  # pylint: disable=W0612
    def mobile_stats_tab_content(state):
        df = stats_table(state)

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
            style_table={"width": "100%",},
            style_header={
                "font-size": "0.65rem",
                "backgroundColor": "#010915",
                "border": "#010915",
                "fontWeight": "bold",
                "font": "Lato, sans-serif",
            },
            style_cell={
                "font-size": "0.65rem",
                "font-family": "Roboto, sans-serif",
                "border-bottom": "0.01rem solid #313841",
                "backgroundColor": "#010915",
                "color": "#FFFFFF",
                "height": "2.5rem",
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
        Output("mobile-us-map", "figure"),
        [
            Input("mobile-map-tabs", "value"),
            Input("mobile-intermediate-value", "children"),
        ],
    )  # pylint: disable=W0612
    def mobile_map_tab_content(value, state):
        """Callback to change between news and twitter feed
        """
        if value == "mobile-testing-us-map-tab":
            return drive_thru_scatter_mapbox(state=REVERSE_STATES_MAP[state])

        return confirmed_scatter_mapbox(state=REVERSE_STATES_MAP[state])

    @app.callback(
        Output("mobile-feed-content-id", "children"),
        [
            Input("mobile-feed-tabs-styled-with-inline", "value"),
            Input("mobile-intermediate-value", "children"),
        ],
    )  # pylint: disable=W0612
    def mobile_feed_tab_content(tab_value, state):
        """Callback to change between news and twitter feed
        """
        if tab_value == "mobile-twitter-tab":
            return twitter_feed(state)

        return news_feed(state)
