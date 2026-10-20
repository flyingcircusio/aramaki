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
from aramaki.db import SqliteDBSessionManager, DBSessionManager

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


class MessageAuthenticationError(Exception):
    pass


class MessageTooOldError(MessageAuthenticationError):
    pass


class InvalidSignatureError(MessageAuthenticationError):
    pass


class Client:
    collections: dict[type[Collection], ReplicationManager]
    subscriptions: dict[str, dict[str, str]]
    callbacks: dict[str, Callable[[dict[str, Any]], Awaitable[Any]]]
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
        callback: Callable[[dict[str, Any]], Awaitable[Any]],
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
                    subscription = {
                        "@type": "aramaki.subscription",
                        "@application": self.application,
                        "matches": [
                            {
                                "@type": type_,
                                "scope": scope,
                            }
                            for type_, scope in self.subscriptions.items()
                        ],
                    }
                    await websocket.send(self.prepare_message(subscription))
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
            parsed_message: dict[str, Any] = json.loads(message)
            self.authenticate(parsed_message)
            if parsed_message.get("@type") in self.callbacks:
                await self.callbacks[parsed_message["@type"]](parsed_message)
        except Exception:
            log.exception("message-processing-failed", message=message)

    def authenticate(self, message: dict[str, Any]) -> None:
        """Authenticate whether this message has originated from the advertised
        principal.

        """
        advertised_principal = message["@principal"]
        assert advertised_principal == "@directory"

        expiry = datetime.datetime.fromisoformat(message["@expiry"])
        # Only accept messages that are not expired
        if expiry < datetime.datetime.now(datetime.UTC):
            raise MessageTooOldError(
                f"message too old (expired at {message['@expiry']})"
            )

        self.known_messages.check(message["@id"])

        check_message = copy.deepcopy(message)
        advertised_signature = check_message["@signature"].pop("signature")

        signature = hmac.new(
            self.secret.encode("ascii"),
            rfc8785.dumps(check_message),
            hashlib.sha256,
        ).hexdigest()

        if signature != advertised_signature:
            raise InvalidSignatureError(
                f"signature mismatch {signature} != {advertised_signature}"
            )
        # Once the message is authenticated, store the ID.
        # This prevents a DOS attack enumerating IDs
        self.known_messages.mark(message["@id"])

    def sign_message(self, message: dict[str, Any]) -> None:
        message["@signature"] = {"alg": "HS256"}
        signature = hmac.new(
            self.secret.encode("ascii"), rfc8785.dumps(message), hashlib.sha256
        ).hexdigest()
        message["@signature"]["signature"] = signature
        log.debug(
            "signing-message",
            type=message.get("@type"),
            id=message.get("@id"),
            signature=signature,
        )

    def prepare_message(self, message: dict[str, Any]) -> str:
        now = utils.now()
        id_ = uuid.uuid4().hex
        log.debug("prepare-message", type=message.get("@type"), id=id_)
        message_template = {
            "@context": "https://flyingcircus.io/ns/aramaki",
            "@version": 1,
            "@principal": self.principal,
            "@application": self.application,
            "@issued": now.isoformat(),
            "@expiry": (now + datetime.timedelta(hours=1)).isoformat(),
            "@id": id_,
        }
        message = copy.deepcopy(message)
        message.update(message_template)
        self.sign_message(message)
        return json.dumps(message)

    async def send_message(self, type: str, message: dict[str, Any]) -> None:
        # TODO: backoff, retry
        # TODO: consider adding (persistent?) buffering
        log.debug("sending-message", status="wait", type=type)
        await self.websocket_ready.wait()
        prepared_message = self.prepare_message(message | {"@type": type})
        assert self.websocket is not None
        await self.websocket.send(prepared_message)
        log.debug("sending-message", status="sent", type=type)

class ClientWithState(Client):
    def __init__(
        self,
        principal: str,
        application: str,
        url: str,
        secret: str,
        db_session_manager: DBSessionManager
    ):
        super().__init__(principal=principal, application=application, url=url, secret=secret)
        self.db = db_session_manager
    
    

