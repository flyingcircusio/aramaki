import asyncio
import json
import logging
import random
import time

import zstd

from aramaki.jobqueue import FederationQueue


async def _main():
    queue = FederationQueue()

    while True:
        message = {
            "messageType": "ping",
            "system": "4f607f0e-ba0f-4d9a-93bf-f9c6dbfcaf99",
            "value": random.randint(1, 1000),
        }
        print(message)
        await queue.incoming(
            zstd.compress(json.dumps(message).encode("utf-8"), 1)
        )
        await asyncio.sleep(1)


def main():
    logging.basicConfig(level=logging.DEBUG)
    while True:
        try:
            asyncio.run(_main())
        except Exception:
            # Make this survive environment restarts
            time.sleep(5)
