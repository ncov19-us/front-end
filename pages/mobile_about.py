import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


mobile_about_body = [
    html.Div([
        html.Div([
            html.H2("What is the Novel Coronavirus?", className="mob-about-page-title"),

            html.Div([
                html.Div([

                    html.Div([
                        html.H3("Coronavirus", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Coronavirus disease (COVID-19) is a respiratory illness which spreads from person to person by droplets from sneezes and coughs. Symptoms can range in severity and they often include a cough, fever, and/or shortness of breath. COVID-19 is caused by a new type of coronavirus that was first identified in 2019 in Wuhan, China."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

                html.Div([], className="about-section-padding"),

                html.Div([

                    html.Div([
                        html.H3("Precautions", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "While there is currently no vaccine or cure for coronavirus disease, proper hygiene is a proven way to avoid catching or spreading COVID-19. Social distancing - avoiding crowds and staying 6+ feet from others in public - has been used to reduce the spread of the disease. Wash your hands with soap and water for at least 20 seconds, especially when in public, and avoid touching your face when your hands aren’t clean."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

            ], className="about-section-container"),

            html.Div([
                html.Div([

                    html.Div([
                        html.H3("Higher Risk", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "While anyone can be diagnosed with coronavirus disease, some people tend to be more at-risk than others. Individuals in the following groups are recommended to take extra precaution to avoid contact with COVID-19: aged 65 years or older, people with weakened immune systems (immunocompromised), living in a nursing home/care facility, other high-risk conditions such as:\n smokers, severe asthma, or chronic lung diseases, heart conditions and/or heart conditions, severe obesity (body mass index or BMI > 40), pregnancy has not shown to increase risk, but pregnant women are, known to be at risk for viral illness and should be monitored"
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

                html.Div([], className="about-section-padding"),

                html.Div([

                    html.Div([
                        html.H3("Spread", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Human-to-human spread is the most common way that people catch COVID-19. The virus is transmitted by droplets from coughs & sneezes that collect on public surfaces and can last up 72 hours. For this reason, the virus is frequently spread when people touch their hands to their face, and proper hygiene & social distancing measures are encouraged to decrease the risk of spreading the virus further."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

            ], className="about-section-container"),

            html.Div([
                html.Div([

                    html.Div([
                        html.H3("Symptoms", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Coronavirus disease can look differently for different people. The most common symptoms are fever, a ‘dry’ cough, and shortness of breath, however some cases of COVID-19 have developed without any obvious symptoms at first. Be sure to get immediate medical assistance if you show any of these emergency symptoms: trouble breathing, persistent pain/pressure in the chest, or bluish lips/face."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

                html.Div([], className="about-section-padding"),

                html.Div([

                    html.Div([
                        html.H3("If You’re Sick", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Social distancing is highly encouraged for anyone suffering from coronavirus disease. This means staying home for the duration of your illness (but visit a clinic/hospital if you’re experiencing a medical emergency). You can receive medical advice and “telecare” over the phone or via video conferencing software (Skype, Zoom, etc). Be sure to wear mask if you do go out in public, and frequently wash your hands with soap & water while in/after leaving public places."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

            ], className="about-section-container")

        ], className="about-page-third", id="about-page-first-third"),

        html.Div([
            html.H2("Where does the data come from?", className="mob-about-page-title"),

            html.Div([
                html.Div([

                    html.Div([
                        html.H3("US Cases", className="about-section-title")
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
                        html.H3("Testing Centers", className="about-section-title")
                    ], className="about-section-title-container"),

                    html.Div([
                        html.P(
                            "Etiam quis quam nec purus mollis finibus. Proin dictum consectetur pellentesque. Pellentesque tincidunt tellus eu iaculis semper. Fusce ac neque maximus, semper risus et, commodo magna. In nulla nibh, fringilla at tincidunt eu, malesuada vehicula mauris. Sed non leo non turpis mattis luctus. Aenean nisl ex, posuere quis turpis a, faucibus scelerisque sapien. Suspendisse vel orci laoreet, maximus neque id, consectetur enim. Donec vitae aliquet leo. In interdum at risus vel facilisis. Donec pulvinar auctor velit. Curabitur nec magna vitae ante placerat tincidunt."
                        , className="about-section-text")
                    ], className="about-section-text-container")
                ], className="about-section"),

            ], className="about-section-container")
        ], className="about-page-third", id="mobile-about-page-second-third"),

        html.Div([
            html.H3("Contributors", id="mob-about-contributors-title"),

            html.H4("Add something about reaching out or something", id="mob-about-contributors-subtitle"),

            html.Div([
                    html.A(href="https://github.com/leehanchung", className="about-contributor-github-icon mob-about-contributor-social-icon"),

                    html.A(href="https://www.linkedin.com/in/hanchunglee/", className="about-contributor-linkedin-icon mob-about-contributor-social-icon"),

                    html.A(href="https://twitter.com/hanchunglee", className="about-contributor-twitter-icon mob-about-contributor-social-icon"),

                html.Div([
                        html.Div("Han Lee", className="mob-about-contributor-name"),

                        html.Div("Data Scientist", className="mob-about-contributor-title")
                     ], className="mob-about-page-contributors")

                ], className="mob-about-page-contributor"),

                html.Div([
                    html.A(href="https://github.com/hurshd0", className="about-contributor-github-icon mob-about-contributor-social-icon"),

                    html.A(href="https://www.linkedin.com/in/hurshd/", className="about-contributor-linkedin-icon mob-about-contributor-social-icon"),

                    html.A(href="https://twitter.com/hurshd0", className="about-contributor-twitter-icon mob-about-contributor-social-icon"),

                html.Div([
                        html.Div("Hursh Desai", className="mob-about-contributor-name"),

                        html.Div("Data Scientist", className="mob-about-contributor-title")
                     ], className="mob-about-page-contributors")

                ], className="mob-about-page-contributor"),

                html.Div([
                    html.A(href="https://github.com/Turtled", className="about-contributor-github-icon mob-about-contributor-social-icon"),

                    html.A(href="https://www.linkedin.com/in/daniel-firpo/", className="about-contributor-linkedin-icon mob-about-contributor-social-icon"),

                    html.A(href="https://twitter.com/danielfirpo2", className="about-contributor-twitter-icon mob-about-contributor-social-icon"),

                html.Div([
                        html.Div("Daniel Firpo", className="mob-about-contributor-name"),

                        html.Div("Web Developer", className="mob-about-contributor-title")
                     ], className="mob-about-page-contributors")

                ], className="mob-about-page-contributor"),

                html.Div([
                    html.A(href="https://github.com/ncov19-us", className="about-contributor-github-icon mob-about-contributor-social-icon"),

                    html.A(href="https://github.com/ncov19-us", className="about-contributor-linkedin-icon mob-about-contributor-social-icon"),

                    html.A(href="https://github.com/ncov19-us", className="about-contributor-twitter-icon mob-about-contributor-social-icon"),

                html.Div([
                        html.Div("Alex Pakalniskis", className="mob-about-contributor-name"),

                        html.Div("Data Scientist", className="mob-about-contributor-title")
                     ], className="mob-about-page-contributors")

                ], className="mob-about-page-contributor"),

                html.Div([
                    html.A(href="https://github.com/mchrupcala", className="about-contributor-github-icon mob-about-contributor-social-icon"),

                    html.A(href="https://www.linkedin.com/in/michaelchrupcala/", className="about-contributor-linkedin-icon mob-about-contributor-social-icon"),

                    html.A(href="https://twitter.com/mikespellcheck", className="about-contributor-twitter-icon mob-about-contributor-social-icon"),

                html.Div([
                        html.Div("Michael Chrupcala", className="mob-about-contributor-name"),

                        html.Div("Web Developer", className="mob-about-contributor-title")
                     ], className="mob-about-page-contributors")

                ], className="mob-about-page-contributor"),

                html.Div([
                    html.A(href="https://github.com/ars394", className="about-contributor-github-icon mob-about-contributor-social-icon"),

                    html.A(href="https://www.linkedin.com/in/anishasunkerneni/", className="about-contributor-linkedin-icon mob-about-contributor-social-icon"),

                    html.A(href="https://twitter.com/youfoundanisha", className="about-contributor-twitter-icon mob-about-contributor-social-icon"),

                html.Div([
                        html.Div("Anisha Sunkerneni", className="mob-about-contributor-name"),

                        html.Div("Web Developer", className="mob-about-contributor-title")
                     ], className="mob-about-page-contributors")

                ], className="mob-about-page-contributor"),

                html.Div([
                    html.A(href="https://github.com/elizabethts", className="about-contributor-github-icon mob-about-contributor-social-icon"),

                    html.A(href="https://www.linkedin.com/in/elizabethts/", className="about-contributor-linkedin-icon mob-about-contributor-social-icon"),

                    html.A(href="https://twitter.com/elizabethts", className="about-contributor-twitter-icon mob-about-contributor-social-icon"),

                html.Div([
                        html.Div("Elizabeth Ter Sahakyan", className="mob-about-contributor-name"),

                        html.Div("Data Scientist", className="mob-about-contributor-title")
                     ], className="mob-about-page-contributors")

                ], className="mob-about-page-contributor")

        ], className="about-page-third", id="about-page-third-third")
    ], id="mobile-about-page")
]