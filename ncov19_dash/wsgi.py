from werkzeug.middleware.dispatcher import DispatcherMiddleware
from .app import server
from .app import app

application = DispatcherMiddleware(server, {
    '/': app.server,
})