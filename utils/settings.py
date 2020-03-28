from decouple import config


# MapBox Token
MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")

# MapBox Style
MAPBOX_STYLE = "mapbox://styles/hurshd0/ck86zky880ory1ip18f5tw4y6"

# ncov19.us API
NCOV19_API = "https://covid19-us-api.herokuapp.com/"

# Drive Thru Facilities
DRIVE_THRU_URL = "https://raw.githubusercontent.com/ncov19-us/ds/master/drive_thru_testing_locations/us-drive-thru-testing-locations.csv"
