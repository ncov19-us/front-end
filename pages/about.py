import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

about_body = [
    html.Div([
        html.Div([
            html.H2("Information about the Novel Coronavirus", className="about-page-title"),

            html.Div([
                html.Div([

                    html.Div([
                        html.H3("Title 1", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

                html.Div([], className="about-section-padding"),

                html.Div([

                    html.Div([
                        html.H3("Title 2", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

            ], className="about-section-container"),

            html.Div([
                html.Div([

                    html.Div([
                        html.H3("Title 1", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

                html.Div([], className="about-section-padding"),

                html.Div([

                    html.Div([
                        html.H3("Title 2", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

            ], className="about-section-container"),

            html.Div([
                html.Div([

                    html.Div([
                        html.H3("Title 1", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

                html.Div([], className="about-section-padding"),

                html.Div([

                    html.Div([
                        html.H3("Title 2", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

            ], className="about-section-container")

        ], className="about-page-third", id="about-page-first-third"),

        html.Div([
            html.H2("Information about the Novel Coronavirus", className="about-page-title"),

            html.Div([
                html.Div([

                    html.Div([
                        html.H3("Title 1", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

                html.Div(className="about-section-padding"),

                html.Div([

                    html.Div([
                        html.H3("Title 2", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

            ], className="about-section-container")
        ], className="about-page-third", id="about-page-second-third"),

        html.Div([
            html.H3("Contributors", id="about-contributors-title"),

            html.H4("Add something about reaching out or something", id="about-contributors-subtitle"),

            html.Div([
                html.Div([

                    html.P("Elizabeth Ter Sahakyan,", className="about-contributor-name"),

                    html.P("Data Scientist", className="about-contributor-title"),

                    html.Img(src="../assets/images/map_1.svg", className="about-contributor-social-icon"),

                    html.Img(src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", className="about-contributor-social-icon"),

                    html.Img(src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", className="about-contributor-social-icon")

                ], className="about-page-contributor")
            ], id="about-page-contributors")

        ], className="about-page-third", id="about-page-third-third")
    ], id="about-page")
]