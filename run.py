from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from ncov19_dash import app as dash_app
from ncov19_dash import server as flask_server

application = DispatcherMiddleware(flask_server, {
    '/': dash_app.server,
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application)
