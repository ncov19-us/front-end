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

# MapBox Token
MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")

# MapBox Style
MAPBOX_STYLE = "mapbox://styles/hurshd0/ck86zky880ory1ip18f5tw4y6"

# Data API URL
NEWS_API_KEY = config("NEWS_API_KEY")
NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

# API Requests for DailyReports
# BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

# API Requests for JHU time series reports
TIME_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

# API Requests for WHO time series reports
WHO_URL = "https://covid.ourworldindata.org/data/total_cases.csv"

# COVID-TRACKING API
CVTRACK_URL = "https://covidtracking.com/api/us"

# https://github.com/javieraviles/covidAPI
TMP_URL = "https://coronavirus-19-api.herokuapp.com/countries/US"


# Drive Thru Facilities
DRIVE_THRU_URL = "https://raw.githubusercontent.com/ncov19-us/ds/master/drive_thru_testing_locations/us-drive-thru-testing-locations.csv"

# Confirmed Stats URL
CONFIRMED_STATS_URL = "https://corona.lmao.ninja/states"

# ncov19.us API
NCOV19_API =  "https://covid19-us-api.herokuapp.com/"