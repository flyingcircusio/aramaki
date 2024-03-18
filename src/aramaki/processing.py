import collections.abc
import json
import logging
import time

import redis
import redis.asyncio
import zstd

import aramaki.monitoring
from aramaki.models.probe import Probe

# Internal/External Message Bus


def json_encode_custom_dicts(obj):
    if isinstance(obj, collections.abc.MutableMapping):
        return dict(obj)
    breakpoint()
    raise TypeError(obj)


def json_dumps_custom_dicts(obj):
    return json.dumps(obj, default=json_encode_custom_dicts)


class UnitOfWork:
    def __init__(self, session, events):
        self.session = session
        self.events = events


class MessageBus:
    REDIS_QUEUE = "messagebus"

    redis: redis.Redis
    aredis: redis.asyncio.Redis  # type: ignore

    def __init__(self, session, redis, aredis):
        self.session = session
        self.aredis = aredis
        self.redis = redis

    async def a_record_external(self, item: str):
        """Record an event on the external message bus.

        (asynchronous version)

        This event will be processed outside of the current transaction
        and will allow other external events to be processed in between.

        """
        logging.debug("placing item in queue")
        await self.aredis.lpush(self.REDIS_QUEUE, item)

    def record_external(self, item: str):
        """Record an event on the external message bus.

        This event will be processed outside of the current transaction
        and will allow other external events to be processed in between.

        """
        logging.debug("placing item in queue")
        self.redis.lpush(self.REDIS_QUEUE, item)

    def process_internal(self, uow):
        """Process all messages on the internal message bus."""
        with uow.session:
            while uow.events:
                event = uow.events.pop()
                aramaki.monitoring.process(uow, event)
            # It's a bit unclear whether committing once per event and thus per
            # aggregate, I guess, is better. I'm batching all internal events
            # get triggered from one external event here but that might be a
            # bad idea, but is likely faster.
            uow.session.commit()

    def process_external(self):
        """Continuously process messages from the external message bus.

        Initializes an empty internal message queue and triggers the
        internal message bus.
        """
        while True:
            item = self.redis.blpop(self.REDIS_QUEUE)
            if item is None:
                continue

            message = json.loads(zstd.decompress(item))
            probe = Probe.from_dict(message)

            uow = UnitOfWork(self.session, [probe])

            self.process_internal(uow)


def process_forever(env):
    while True:
        try:
            bus = MessageBus(
                env["request"].dbsession,
                env["request"].redis,
                env["request"].aredis,
            )
            bus.process_external()
        except Exception:
            logging.exception(
                "Encountered error in external message bus processing"
            )
            time.sleep(10)
