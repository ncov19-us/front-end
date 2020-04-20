###############################################################################
# 2020-04-15: Han:
#
# To run the app using Flask directly, please set environment variable with
# $Env:FLASK_APP='ncov19_dash:server' for windows, or
# export FLASK_APP=ncov19_dash:server for Linux.
#
# And `flask run` to run the app. Alternatively, do `python run.py` at the
# project root directory for dev mode.
#
# Set default config to ProductionConfig unless STAGING environment
# is set to true on Linux `export STAGING=True` or Windows Powershell
# `$Env:STAGING="True"`. Using os.environ directly will throw errors
# if not set.
#
# Changing the order of the imports might cause circular import problem.
# Flask server is created before dash app to allow proper flask routing.
###############################################################################
from ncov19_dash.config import PACKAGE_ROOT, config
from ncov19_dash.cache import server_cache
from ncov19_dash.flask_server import server
from ncov19_dash.dash_app import app


with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()
