import tweepy
from decouple import config
from utils import CovidMongo, TwitterMongo


# Mongo DB
DB_NAME = "covid"
COLLECTION_STATE = "state"
COLLECTION_TWITTER = "twitter"

# Connect to MongoDB
cm = CovidMongo(DB_NAME, COLLECTION_STATE, verbose=False)
tm = TwitterMongo(DB_NAME, COLLECTION_TWITTER, verbose=False)

# Tweepy
TWITTER_AUTH = tweepy.OAuthHandler(
    config("TWITTER_CONSUMER_KEY"), config("TWITTER_CONSUMER_SECRET_KEY")
)
TWITTER_AUTH.set_access_token(
    config("TWITTER_ACCESS_TOKEN"), config("TWITTER_ACCESS_TOKEN_SECRET")
)
TWITTER = tweepy.API(TWITTER_AUTH)

# Plotly Dash
DEFAULT_OPACITY = 0.8
theme = {
    "dark": True,
    "detail": "#007439",
    "primary": "#00EA64",
    "secondary": "#6E6E6E",
}


# MapBox Token
MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")

# Data API URL
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=us&apiKey=da8e2e705b914f9f86ed2e9692e66012"

# API Requests for DailyReports
BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

# API Requests for JHU time series reports
TIME_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

# API Requests for WHO time series reports
WHO_URL = "https://covid.ourworldindata.org/data/total_cases.csv"

# COVID-TRACKING API
CVTRACK_URL = "https://covidtracking.com/api/us/daily"

# https://github.com/javieraviles/covidAPI
TMP_URL = "https://coronavirus-19-api.herokuapp.com/countries/US"
