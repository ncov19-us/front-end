import flask

from ncov19_dash.cache import server_cache
from ncov19_dash import config
from ncov19_dash.routes import sitemap
from ncov19_dash.routes import robots


###############################################################################
#
#    Initialize Flask server
#
###############################################################################
server = flask.Flask(__name__, static_folder="assets",)
server.secret_key = config.SECRET_KEY
server.config["TESTING"] = config.TESTING
server_cache.init_app(server)

server.register_blueprint(sitemap)
server.register_blueprint(robots)
