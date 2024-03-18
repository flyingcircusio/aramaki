import redis
import redis.asyncio


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    """

    config.include("aramaki.models")

    def get_redis(request):
        return redis.Redis.from_url(request.registry.settings["redis.url"])

    config.add_request_method(get_redis, "redis", reify=True)

    def get_async_redis(request):
        return redis.asyncio.Redis.from_url(
            request.registry.settings["redis.url"]
        )

    config.add_request_method(get_async_redis, "aredis", reify=True)
