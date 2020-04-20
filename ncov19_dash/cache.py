###############################################################################
#
# 2020-04-15 Han: Caching has to be abstracted out to avoid circular imports.
# When caching is implemented inside __init__.py, flask_server.py, or
# dash_app.py, the components will have to import the app/server, creating
# circular import problems.
#
################################################################################
from flask_caching import Cache


server_cache = Cache(
    config={
        "CACHE_TYPE": "filesystem",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_DIR": "cache",
    },
)
