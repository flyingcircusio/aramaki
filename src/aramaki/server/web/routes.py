import time

from pyramid.static import QueryStringConstantCacheBuster


def includeme(config):
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_cache_buster(
        "static", QueryStringConstantCacheBuster(str(int(time.time())))
    )

    config.add_route("dashboard", "/")
