import os
import pathlib
from decouple import config


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent


class StagingConfig:
    """Base config, uses staging API"""

    DEBUG = True
    TESTING = True

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


class ProductionConfig(StagingConfig):
    """Uses production database server."""

    DEBUG = False
    TESTING = False

    # ncov19.us API
    NCOV19_API = config("NCOV19_PROD_API")

    # Drive Thru Facilities
    DRIVE_THRU_URL = config("DRIVE_THRU_PROD_URL")

    # MapBox Style
    MAPBOX_STYLE = config("MAPBOX_PRODUCTION_STYLE")


# Set default config to ProductionConfig unless STAGING environment
# is set to true on Linux `export STAGING=True` or Windows Powershell
# `$Env:STAGING="True"`. Using os.environ directly will throw errors
# if not set.
def get_config():
    STAGING = os.getenv("STAGING") or "False"

    if STAGING == "True":
        return StagingConfig

    return ProductionConfig

config = get_config()
