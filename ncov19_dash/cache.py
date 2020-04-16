from flask_caching import Cache


server_cache = Cache(
    config={
        "CACHE_TYPE": "filesystem",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_DIR": "cache",
    },
)
