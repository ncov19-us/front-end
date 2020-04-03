from decouple import config


# MapBox Token
MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")

# MapBox Style
MAPBOX_STYLE = "mapbox://styles/hurshd0/ck86zky880ory1ip18f5tw4y6"

# ncov19.us API
# NCOV19_API = "https://covid19-us-api.herokuapp.com/"
NCOV19_API = "https://44f38618.ngrok.io/"
# NCOV19_API = "https://covid19-us-api-staging.herokuapp.com/"

# Drive Thru Facilities
DRIVE_THRU_URL = "https://raw.githubusercontent.com/ncov19-us/ds/master/drive_thru_testing_locations/us-drive-thru-testing-locations.csv"


STATES_LAT_LONG = [
    {"state": "Alabama", "latitude": 32.806671, "longitude": -86.791130},
    {"state": "Alaska", "latitude": 61.370716, "longitude": -152.404419},
    {"state": "Arizona", "latitude": 33.729759, "longitude": -111.431221},
    {"state": "Arkansas", "latitude": 34.969704, "longitude": -92.373123},
    {"state": "California", "latitude": 36.116203, "longitude": -119.681564},
    {"state": "Colorado", "latitude": 39.059811, "longitude": -105.311104},
    {"state": "Connecticut", "latitude": 41.597782, "longitude": -72.755371},
    {"state": "Delaware", "latitude": 39.318523, "longitude": -75.507141},
    {"state": "District of Columbia", "latitude": 38.897438, "longitude": -77.026817},
    {"state": "Florida", "latitude": 27.766279, "longitude": -81.686783},
    {"state": "Georgia", "latitude": 33.040619, "longitude": -83.643074},
    {"state": "Hawaii", "latitude": 21.094318, "longitude": -157.498337},
    {"state": "Idaho", "latitude": 44.240459, "longitude": -114.478828},
    {"state": "Illinois", "latitude": 40.349457, "longitude": -88.986137},
    {"state": "Indiana", "latitude": 39.849426, "longitude": -86.258278},
    {"state": "Iowa", "latitude": 42.011539, "longitude": -93.210526},
    {"state": "Kansas", "latitude": 38.526600, "longitude": -96.726486},
    {"state": "Kentucky", "latitude": 37.668140, "longitude": -84.670067},
    {"state": "Louisiana", "latitude": 31.169546, "longitude": -91.867805},
    {"state": "Maine", "latitude": 44.693947, "longitude": -69.381927},
    {"state": "Maryland", "latitude": 39.063946, "longitude": -76.802101},
    {"state": "Massachusetts", "latitude": 42.230171, "longitude": -71.530106},
    {"state": "Michigan", "latitude": 43.326618, "longitude": -84.536095},
    {"state": "Minnesota", "latitude": 45.694454, "longitude": -93.900192},
    {"state": "Mississippi", "latitude": 32.741646, "longitude": -89.678696},
    {"state": "Missouri", "latitude": 38.456085, "longitude": -92.288368},
    {"state": "Montana", "latitude": 46.921925, "longitude": -110.454353},
    {"state": "Nebraska", "latitude": 41.125370, "longitude": -98.268082},
    {"state": "Nevada", "latitude": 38.313515, "longitude": -117.055374},
    {"state": "New Hampshire", "latitude": 43.452492, "longitude": -71.563896},
    {"state": "New Jersey", "latitude": 40.298904, "longitude": -74.521011},
    {"state": "New Mexico", "latitude": 34.840515, "longitude": -106.248482},
    {"state": "New York", "latitude": 42.165726, "longitude": -74.948051},
    {"state": "North Carolina", "latitude": 35.630066, "longitude": -79.806419},
    {"state": "North Dakota", "latitude": 47.528912, "longitude": -99.784012},
    {"state": "Ohio", "latitude": 40.388783, "longitude": -82.764915},
    {"state": "Oklahoma", "latitude": 35.565342, "longitude": -96.928917},
    {"state": "Oregon", "latitude": 44.572021, "longitude": -122.070938},
    {"state": "Pennsylvania", "latitude": 40.590752, "longitude": -77.209755},
    {"state": "Rhode Island", "latitude": 41.680893, "longitude": -71.511780},
    {"state": "South Carolina", "latitude": 33.856892, "longitude": -80.945007},
    {"state": "South Dakota", "latitude": 44.299782, "longitude": -99.438828},
    {"state": "Tennessee", "latitude": 35.747845, "longitude": -86.692345},
    {"state": "Texas", "latitude": 31.054487, "longitude": -97.563461},
    {"state": "Utah", "latitude": 40.150032, "longitude": -111.862434},
    {"state": "Vermont", "latitude": 44.045876, "longitude": -72.710686},
    {"state": "Virginia", "latitude": 37.769337, "longitude": -78.169968},
    {"state": "Washington", "latitude": 47.400902, "longitude": -121.490494},
    {"state": "West Virginia", "latitude": 38.491226, "longitude": -80.954453},
    {"state": "Wisconsin", "latitude": 44.268543, "longitude": -89.616508},
    {"state": "Wyoming", "latitude": 42.755966, "longitude": -107.302490},
]

STATES_COORD = {
    "United States": {
        "latitude": 39.8097343,
        "longitude": -98.5556199,
        "zoom": 2,
        "stateAbbr": "US",
    },
    "Alabama": {
        "latitude": 32.806671,
        "longitude": -86.791130,
        "zoom": 5.5,
        "stateAbbr": "AL",
    },
    "Alaska": {
        "latitude": 61.370716,
        "longitude": -152.404419,
        "zoom": 3,
        "stateAbbr": "AK",
    },
    "Arizona": {
        "latitude": 33.729759,
        "longitude": -111.431221,
        "zoom": 5,
        "stateAbbr": "AZ",
    },
    "Arkansas": {
        "latitude": 34.969704,
        "longitude": -92.373123,
        "zoom": 5.5,
        "stateAbbr": "AR",
    },
    "California": {
        "latitude": 36.116203,
        "longitude": -119.681564,
        "zoom": 4,
        "stateAbbr": "CA",
    },
    "Colorado": {
        "latitude": 39.059811,
        "longitude": -105.311104,
        "zoom": 5.5,
        "stateAbbr": "CO",
    },
    "Connecticut": {
        "latitude": 41.597782,
        "longitude": -72.755371,
        "zoom": 6.5,
        "stateAbbr": "CT",
    },
    "Delaware": {
        "latitude": 39.318523,
        "longitude": -75.507141,
        "zoom": 6.5,
        "stateAbbr": "DE",
    },
    "District Of Columbia": {
        "latitude": 38.897438,
        "longitude": -77.026817,
        "zoom": 8,
        "stateAbbr": "DC",
    },
    "Florida": {
        "latitude": 27.766279,
        "longitude": -81.686783,
        "zoom": 5.5,
        "stateAbbr": "FL",
    },
    "Georgia": {
        "latitude": 33.040619,
        "longitude": -83.643074,
        "zoom": 6,
        "stateAbbr": "GA",
    },
    "Guam": {"latitude": 13.4443, "longitude": 144.7937, "zoom": 9, "stateAbbr": "GU",},
    "Hawaii": {
        "latitude": 21.094318,
        "longitude": -157.498337,
        "zoom": 5.5,
        "stateAbbr": "HI",
    },
    "Idaho": {
        "latitude": 44.240459,
        "longitude": -114.478828,
        "zoom": 5.5,
        "stateAbbr": "ID",
    },
    "Illinois": {
        "latitude": 40.349457,
        "longitude": -88.986137,
        "zoom": 5,
        "stateAbbr": "IL",
    },
    "Indiana": {
        "latitude": 39.849426,
        "longitude": -86.258278,
        "zoom": 5.5,
        "stateAbbr": "IN",
    },
    "Iowa": {
        "latitude": 42.011539,
        "longitude": -93.210526,
        "zoom": 5.5,
        "stateAbbr": "IA",
    },
    "Kansas": {
        "latitude": 38.526600,
        "longitude": -96.726486,
        "zoom": 5.5,
        "stateAbbr": "KS",
    },
    "Kentucky": {
        "latitude": 37.668140,
        "longitude": -84.670067,
        "zoom": 5.2,
        "stateAbbr": "KY",
    },
    "Louisiana": {
        "latitude": 31.169546,
        "longitude": -91.867805,
        "zoom": 6,
        "stateAbbr": "LA",
    },
    "Maine": {
        "latitude": 44.693947,
        "longitude": -69.381927,
        "zoom": 5.5,
        "stateAbbr": "ME",
    },
    "Maryland": {
        "latitude": 39.063946,
        "longitude": -76.802101,
        "zoom": 6.5,
        "stateAbbr": "MD",
    },
    "Massachusetts": {
        "latitude": 42.230171,
        "longitude": -71.530106,
        "zoom": 6.5,
        "stateAbbr": "MA",
    },
    "Michigan": {
        "latitude": 43.326618,
        "longitude": -84.536095,
        "zoom": 5.5,
        "stateAbbr": "MI",
    },
    "Minnesota": {
        "latitude": 45.694454,
        "longitude": -93.900192,
        "zoom": 5,
        "stateAbbr": "MN",
    },
    "Mississippi": {
        "latitude": 32.741646,
        "longitude": -89.678696,
        "zoom": 5.5,
        "stateAbbr": "MS",
    },
    "Missouri": {
        "latitude": 38.456085,
        "longitude": -92.288368,
        "zoom": 5.5,
        "stateAbbr": "MO",
    },
    "Montana": {
        "latitude": 46.921925,
        "longitude": -110.454353,
        "zoom": 5,
        "stateAbbr": "MT",
    },
    "Nebraska": {
        "latitude": 41.125370,
        "longitude": -98.268082,
        "zoom": 5,
        "stateAbbr": "NE",
    },
    "Nevada": {
        "latitude": 38.313515,
        "longitude": -117.055374,
        "zoom": 4.5,
        "stateAbbr": "NV",
    },
    "New Hampshire": {
        "latitude": 43.452492,
        "longitude": -71.563896,
        "zoom": 7,
        "stateAbbr": "NH",
    },
    "New Jersey": {
        "latitude": 40.298904,
        "longitude": -74.521011,
        "zoom": 6,
        "stateAbbr": "NJ",
    },
    "New Mexico": {
        "latitude": 34.840515,
        "longitude": -106.248482,
        "zoom": 5,
        "stateAbbr": "NM",
    },
    "New York": {
        "latitude": 42.165726,
        "longitude": -74.948051,
        "zoom": 5.5,
        "stateAbbr": "NY",
    },
    "North Carolina": {
        "latitude": 35.630066,
        "longitude": -79.806419,
        "zoom": 5.5,
        "stateAbbr": "NC",
    },
    "North Dakota": {
        "latitude": 47.528912,
        "longitude": -99.784012,
        "zoom": 5,
        "stateAbbr": "ND",
    },
    "Ohio": {
        "latitude": 40.388783,
        "longitude": -82.764915,
        "zoom": 5.5,
        "stateAbbr": "OH",
    },
    "Oklahoma": {
        "latitude": 35.565342,
        "longitude": -96.928917,
        "zoom": 5.5,
        "stateAbbr": "OK",
    },
    "Oregon": {
        "latitude": 44.572021,
        "longitude": -122.070938,
        "zoom": 5,
        "stateAbbr": "OR",
    },
    "Pennsylvania": {
        "latitude": 40.590752,
        "longitude": -77.209755,
        "zoom": 5.5,
        "stateAbbr": "PA",
    },
    "Puerto Rico": {
        "latitude": 18.2208,
        "longitude": -66.5901,
        "zoom": 5.5,
        "stateAbbr": "PR",
    },
    "Rhode Island": {
        "latitude": 41.680893,
        "longitude": -71.511780,
        "zoom": 6.5,
        "stateAbbr": "RI",
    },
    "South Carolina": {
        "latitude": 33.856892,
        "longitude": -80.945007,
        "zoom": 5.5,
        "stateAbbr": "SC",
    },
    "South Dakota": {
        "latitude": 44.299782,
        "longitude": -99.438828,
        "zoom": 5.5,
        "stateAbbr": "SD",
    },
    "Tennessee": {
        "latitude": 35.747845,
        "longitude": -86.692345,
        "zoom": 5.5,
        "stateAbbr": "TN",
    },
    "Texas": {
        "latitude": 31.054487,
        "longitude": -97.563461,
        "zoom": 4.5,
        "stateAbbr": "TX",
    },
    "Utah": {
        "latitude": 40.150032,
        "longitude": -111.862434,
        "zoom": 4.5,
        "stateAbbr": "UT",
    },
    "Vermont": {
        "latitude": 44.045876,
        "longitude": -72.710686,
        "zoom": 7,
        "stateAbbr": "VT",
    },
    "Virginia": {
        "latitude": 37.769337,
        "longitude": -78.169968,
        "zoom": 6,
        "stateAbbr": "VA",
    },
    "Washington": {
        "latitude": 47.400902,
        "longitude": -121.490494,
        "zoom": 5,
        "stateAbbr": "WA",
    },
    "West Virginia": {
        "latitude": 38.491226,
        "longitude": -80.954453,
        "zoom": 6.2,
        "stateAbbr": "WV",
    },
    "Wisconsin": {
        "latitude": 44.268543,
        "longitude": -89.616508,
        "zoom": 4.5,
        "stateAbbr": "WI",
    },
    "Wyoming": {
        "latitude": 42.755966,
        "longitude": -107.302490,
        "zoom": 5,
        "stateAbbr": "WY",
    },
}


REVERSE_STATES_MAP = {}
for k, v in STATES_COORD.items():
    REVERSE_STATES_MAP[v["stateAbbr"]] = k
