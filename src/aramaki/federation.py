import asyncio

import websockets

from aramaki.processing import MessageBus


async def server(env):
    async def handle_federation(websocket):
        """Handle processing of a single websocket connection.

        On the incoming side this basically places things into the federation
        queue.

        On the outgoing side this basically pulls things from the federation
        queue and sends them out over the appropriate federation sockets.

        We want to scale out as much processing onto the job queue as possible
        as that is something we'd like to be able to scale horizontally,
        potentially over multiple nodes.

        Scaling the federation handler would be possible behind a load balancer
        and/or using the SO_REUSE socket option.

        To reduce processing requirements in this process there is no
        verification, no decompression or anything going on, just simply
        placing the messages into a redis queue.

        """
        bus = MessageBus(
            None,  # no database here
            None,  # no syncronous redis here
            env["request"].aredis,
        )
        while True:
            message = await websocket.recv()
            # XXX Security: we need some kind of authorization and potentially
            # rate limiting. However, this would only be abuse/DOS protection,
            # not anything CPU intensive like validating with the database,
            # which should happen in the processing environment.
            asyncio.create_task(bus.a_record_external(message))

    # XXX make configurable
    async with websockets.serve(handle_federation, "0.0.0.0", 8764):
        await asyncio.Future()  # run forever
