from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from ncov19_dash import app
from ncov19_dash import server

print('finishing importing...')
app.enable_dev_tools(debug=True)
print('finishing setting debug mode...')

application = DispatcherMiddleware(server, {
    '/': app.server,
})

print('finishing middleware app...')

if __name__ == '__main__':
    run_simple('localhost', 8050, application)
