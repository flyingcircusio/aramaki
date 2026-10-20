import asyncio
import copy
import datetime
import hashlib
import hmac
import json
import random
import time
import uuid
from asyncio import CancelledError
from collections import deque
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import rfc8785
import structlog.stdlib
import websockets
from websockets import ClientConnection
from websockets.exceptions import WebSocketException

from aramaki import utils
from aramaki.collection import Collection, ReplicationManager
from aramaki.db import DBSessionManager, SqliteDBSessionManager
from aramaki.message import (
    Message,
    SubscriptionMatch,
    SubscriptionMessage,
    message_adapter,
)

log = structlog.stdlib.get_logger()


class MessageReplaySet:
    ids: set[str]
    ages: deque[tuple[float, str]]  # monotonic increasing timestamp from left to right

    EXPIRE_INTERVAL = 60
    TIMEOUT = 60 * 60 + 5 * 60  # 1h 5m

    def __init__(self) -> None:
        self.ids = set()
        self.ages = deque()
        self.last_expire = time.time()

    def check(self, id: str) -> None:
        if self.last_expire < time.time() - self.EXPIRE_INTERVAL:
            self.expire()
        if id in self.ids:
            raise KeyError(f"ID already seen: {id}")

    def mark(self, id: str) -> None:
        self.ids.add(id)
        self.ages.append((time.time(), id))

    def expire(self) -> None:
        cutoff = time.time() - self.TIMEOUT
        while self.ages:
            t, id = self.ages.popleft()
            if t > cutoff:
                self.ages.appendleft((t, id))
                break
            self.ids.remove(id)
        self.last_expire = time.time()


class Client:
    collections: dict[type[Collection], ReplicationManager]
    subscriptions: dict[str, dict[str, str]]
    callbacks: dict[str, Callable[[Message], Awaitable[Any]]]
    tasks: set[asyncio.Task[Any]]

    def __init__(
        self,
        principal: str,
        application: str,
        url: str,
        secret: str,
    ):
        self.websocket: ClientConnection | None = None
        self.known_messages = MessageReplaySet()
        self.principal = principal
        self.application = application
        self.url = url
        self.secret = secret

        self.subscriptions = {}
        self.callbacks = {}
        self.tasks = set()
        self.websocket_ready = asyncio.Event()

        self.collections = {}

    def register_message_handler(
        self,
        type_: str,
        callback: Callable[[Message], Awaitable[Any]],
        **scope: str,
    ) -> None:
        self.subscriptions[type_] = scope
        self.callbacks[type_] = callback

    def register_collection(self, cls_: type["Collection"]) -> ReplicationManager:
        """Activate a collection and provide a factory that can be used with `svcs`."""
        assert cls_ not in self.collections
        self.collections[cls_] = manager = ReplicationManager(self, cls_)
        return manager

    async def run(self) -> None:
        log.info("start-manager")

        connection_errors = 0

        while True:
            try:
                log.info("directory-connection", status="connecting")
                async with websockets.connect(self.url) as websocket:
                    connection_errors = 0
                    self.websocket = websocket
                    log.info("directory-connection", status="connected")
                    subscription = SubscriptionMessage(
                        application=self.application,
                        principal=self.principal,
                        matches=[
                            SubscriptionMatch(type=type_, scope=scope)
                            for type_, scope in self.subscriptions.items()
                        ],
                    )
                    self.sign_message(subscription)
                    await websocket.send(subscription.model_dump_json())
                    log.info("subscriptions", status="sent")
                    self.websocket_ready.set()

                    log.info("Waiting for messages ...")
                    async for message in websocket:
                        if isinstance(message, bytes):
                            message = message.decode("utf-8")
                        utils.create_task(self.process(message))
            except CancelledError:
                return
            except (WebSocketException, ConnectionError) as e:
                connection_errors += 1
                log.error("connection error", type=str(type(e).__name__), error=str(e))
            except Exception:
                connection_errors += 1
                log.exception("unexpected-exception")
            finally:
                self.websocket_ready.clear()
                self.websocket = None
            backoff = random.randint(0, int(1.5 ** min([10, connection_errors])))
            log.info("connection lost", backoff=backoff, errors=connection_errors)
            await asyncio.sleep(backoff)

    def start(self) -> None:
        self.tasks.add(utils.create_task(self.run()))

    def stop(self) -> None:
        for collection in self.collections.values():
            collection.stop()
        for task in self.tasks:
            task.cancel()

    async def process(self, message: str) -> None:
        try:
            parsed_message = message_adapter.validate_json(
                message, context={"allow_defaults": False}
            )
            self.authenticate(parsed_message)
            callback = self.callbacks.get(parsed_message.type)
            if callback:
                await callback(parsed_message)
        except Exception:
            log.exception("message-processing-failed", message=message)

    def authenticate(self, message: Message) -> None:
        """Authenticate whether this message has originated from the advertised
        principal.

        """
        advertised_principal = message.principal
        assert advertised_principal == "@directory"

        self.known_messages.check(message.id)
        message.authenticate(self.secret.encode("ascii"))

        # Once the message is authenticated, store the ID.
        # This prevents a DOS attack enumerating IDs
        self.known_messages.mark(message.id)

    def sign_message(self, message: Message) -> None:
        message.sign(self.secret.encode("ascii"))

    async def send_message(self, message: Message) -> None:
        # TODO: backoff, retry
        # TODO: consider adding (persistent?) buffering
        log.debug("sending-message", status="wait", type=message.type)
        await self.websocket_ready.wait()
        self.sign_message(message)
        assert self.websocket is not None
        await self.websocket.send(message.model_dump_json())
        log.debug("sending-message", status="sent", type=message.type)


class ClientWithState(Client):
    def __init__(
        self,
        principal: str,
        application: str,
        url: str,
        secret: str,
        db_session_manager: DBSessionManager,
    ):
        super().__init__(
            principal=principal, application=application, url=url, secret=secret
        )
        self.db = db_session_manager
