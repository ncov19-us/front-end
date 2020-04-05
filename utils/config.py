from decouple import config


class Config(object):
    """Base config, uses staging API"""

    DEBUG = False
    TESTING = False

    # Secret Key
    SECRET_KEY = config("SECRET_KEY")

    # MapBox Token
    MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")

    # MapBox Style
    MAPBOX_STYLE = config("MAPBOX_STAGING_STYLE")

    # ncov19.us API
    NCOV19_API = config("NCOV19_STAGING_API")

    # Add routes here
    COUNTY = "county"
    TWITTER = "twitter"
    STATS = "stats"
    COUNTRY = "country"
    STATE = "state"
    NEWS = "news"

    # Drive Thru Facilities
    DRIVE_THRU_URL = config("DRIVE_THRU_STAGING_URL")


class ProductionConfig(Config):
    """Uses production database server."""

    DEBUG = False
    TESTING = False

    # ncov19.us API
    NCOV19_API = config("NCOV19_PROD_API")

    # Drive Thru Facilities
    DRIVE_THRU_URL = config("DRIVE_THRU_PROD_URL")

    # MapBox Style
    MAPBOX_STYLE = config("MAPBOX_PRODUCTION_STYLE")
