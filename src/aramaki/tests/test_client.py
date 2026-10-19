import asyncio
import datetime
import json
import time
import unittest.mock
import uuid
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any

import pytest
import websockets

from aramaki.client import (
    Client,
    InvalidSignatureError,
    MessageReplaySet,
    MessageTooOldError,
)
from aramaki.typing import JSONObject


@pytest.fixture
def now(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[unittest.mock.Mock]:
    now = unittest.mock.Mock()
    now.return_value = 0

    class MockedDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz: datetime.tzinfo | None = None) -> "MockedDateTime":
            return cls.fromtimestamp(now.return_value, tz)

    monkeypatch.setattr(time, "time", now)
    monkeypatch.setattr(datetime, "datetime", MockedDateTime)
    yield now


def test_now_mock(now: unittest.mock.Mock):
    assert time.time() == 0
    assert (
        datetime.datetime.now(datetime.UTC).isoformat() == "1970-01-01T00:00:00+00:00"
    )


def test_message_replay_set(now: unittest.mock.Mock):
    set = MessageReplaySet()

    # An unknown id doesn't trigger
    set.check("asdf")

    # An ID that was marked does trigger
    set.mark("asdf")
    with pytest.raises(KeyError):
        set.check("asdf")

    assert "asdf" in set.ids

    # If we go past the timeout an automatic expiry will run
    # and the key will be forgotten
    now.return_value += set.TIMEOUT + 1

    set.check("asdf")

    assert "asdf" not in set.ids


def test_message_replay_set_expire_interval_triggerd(
    now: unittest.mock.Mock,
):
    set = MessageReplaySet()
    assert set.last_expire == now()

    # Calling check after the expire interval causes
    # an expiry to run and the timestamp to update.
    now.return_value += set.EXPIRE_INTERVAL + 1
    assert set.last_expire < now()
    set.check("asdf")
    assert set.last_expire == now()

    # Calling check before the expire interval causes
    # no expiry

    now.return_value += set.EXPIRE_INTERVAL - 5
    set.check("asdf")
    assert set.last_expire < now()


def test_message_replay_set_expire_only_outdated(
    now: unittest.mock.Mock,
):
    set = MessageReplaySet()
    # Mark two IDs distributed so that we can move time forward
    # and expire one, but not the other
    set.mark("asdf")
    now.return_value += set.TIMEOUT - 100
    set.mark("bsdf")

    # Both IDs now do not pass the test.
    with pytest.raises(KeyError):
        set.check("asdf")
    with pytest.raises(KeyError):
        set.check("bsdf")

    # Move time forward so the first mark expires
    now.return_value += 200

    # The first mark now passes the check again, but the second
    # doesn't.
    set.check("asdf")
    with pytest.raises(KeyError):
        set.check("bsdf")


async def test_client_authenticate(now: unittest.mock.Mock, tmp_path: Path):
    client = Client("host1", "app", "dummy", "asdf", tmp_path)

    # Start assembling a message until we pass it. This needs
    # 1. A proper principal
    message: JSONObject = {"@principal": "foobar"}
    with pytest.raises(AssertionError):
        client.authenticate(message)

    message["@principal"] = "@directory"

    # 2. A non-outdated expiry
    message["@expiry"] = (
        datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    ).isoformat()
    with pytest.raises(MessageTooOldError) as e:
        client.authenticate(message)
    assert "message too old" in e.value.args[0]

    message["@expiry"] = (
        datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    ).isoformat()

    # 3. An unknown ID
    message["@id"] = "unknown message"
    # 3. And a proper signature
    message["@signature"] = {"signature": "asdf"}
    with pytest.raises(InvalidSignatureError):
        client.authenticate(message)

    message["@signature"] = {
        "alg": "HS256",
        "signature": "4e864a961345d3080666c434ff466e7394280f64ba53d6e2ae52da47d836c4c5",
    }
    client.authenticate(message)

    del message["@signature"]
    client.sign_message(message)
    assert message["@signature"] == {
        "alg": "HS256",
        "signature": "4e864a961345d3080666c434ff466e7394280f64ba53d6e2ae52da47d836c4c5",
    }


async def test_client_stop_start(tmp_path: Path):
    client = Client("host1", "app", "dummy", "asdf", tmp_path)
    client.start()
    client.stop()


async def test_client_creates_new_dir(tmp_path: Path):
    dir = tmp_path / "new"
    assert not dir.exists()
    Client("host1", "app", "dummy", "asdf", dir)
    assert dir.exists()


async def test_client_prepare_message(
    now: unittest.mock.Mock, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    client = Client("host1", "app", "dummy", "asdf", tmp_path)

    m_uuid = unittest.mock.Mock()
    m_uuid().hex = "64473ce93de046988f93a3feb6e11914"
    monkeypatch.setattr(uuid, "uuid4", m_uuid)
    message = client.prepare_message({"key": "value"})

    message = json.loads(message)
    assert message == {
        "key": "value",
        "@context": "https://flyingcircus.io/ns/aramaki",
        "@version": 1,
        "@principal": "host1",
        "@application": "app",
        "@issued": "1970-01-01T00:00:00+00:00",
        "@expiry": "1970-01-01T01:00:00+00:00",
        "@id": "64473ce93de046988f93a3feb6e11914",
        "@signature": {
            "alg": "HS256",
            "signature": "48a5dceadf3593a2db2ef97c60bbe05546b357ca07a762c873f5f516210e5443",
        },
    }


async def test_client_process_message(
    now: unittest.mock.Mock, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    client = Client("host1", "app", "dummy", "asdf", tmp_path)

    seen_messages: list[JSONObject] = []

    async def handle_message(message: JSONObject) -> None:
        seen_messages.append(message)

    client.register_message_handler("message", handle_message)
    message: JSONObject = {
        "key": "value",
        "@type": "message",
        "@context": "https://flyingcircus.io/ns/aramaki",
        "@version": 1,
        "@principal": "@directory",
        "@application": "app",
        "@issued": "1970-01-01T00:00:00+00:00",
        "@expiry": "1970-01-01T01:00:00+00:00",
        "@id": "64473ce93de046988f93a3feb6e11914",
        "@signature": {
            "alg": "HS256",
            "signature": "071020c8662b940949ee6c76bca47a8c81c53eda526d0139196e0fb98c8b2f9d",
        },
    }
    client.sign_message(message)

    await client.process(json.dumps(message))

    assert len(seen_messages) == 1
    assert seen_messages[0] == {
        "@application": "app",
        "@context": "https://flyingcircus.io/ns/aramaki",
        "@expiry": "1970-01-01T01:00:00+00:00",
        "@id": "64473ce93de046988f93a3feb6e11914",
        "@issued": "1970-01-01T00:00:00+00:00",
        "@principal": "@directory",
        "@signature": {
            "alg": "HS256",
            "signature": "071020c8662b940949ee6c76bca47a8c81c53eda526d0139196e0fb98c8b2f9d",
        },
        "@type": "message",
        "@version": 1,
        "key": "value",
    }


async def test_client_process_with_missing_or_unknown_type_ignored(
    now: unittest.mock.Mock, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    client = Client("host1", "app", "dummy", "asdf", tmp_path)

    message: JSONObject = {
        "key": "value",
        "@context": "https://flyingcircus.io/ns/aramaki",
        "@version": 1,
        "@type": "unknown",
        "@principal": "@directory",
        "@application": "app",
        "@issued": "1970-01-01T00:00:00+00:00",
        "@expiry": "1970-01-01T01:00:00+00:00",
        "@id": "64473ce93de046988f93a3feb6e11914",
        "@signature": {
            "alg": "HS256",
            "signature": "071020c8662b940949ee6c76bca47a8c81c53eda526d0139196e0fb98c8b2f9d",
        },
    }
    client.sign_message(message)
    await client.process(json.dumps(message))

    del message["@type"]
    assert isinstance(message["@id"], str)
    message["@id"] += "a"  # make a new id
    client.sign_message(message)
    await client.process(json.dumps(message))


class AsyncContextClientMock:
    """Mock for async context clients with nested mocking capabilities."""

    def __init__(self, mock: unittest.mock.AsyncMock):
        """Initialize with a mock that will be returned from __aenter__."""
        self.mock = mock

    async def __aenter__(self) -> unittest.mock.AsyncMock:
        """Enter async context client."""
        return self.mock

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> None:
        """Exit async context client."""


async def test_client_run_loop(
    now: unittest.mock.Mock, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    websocket = unittest.mock.AsyncMock()
    connect = unittest.mock.Mock()
    connect.return_value = AsyncContextClientMock(websocket)
    monkeypatch.setattr(websockets, "connect", connect)

    async def receive_messages(self: Any) -> AsyncGenerator[bytes]:
        yield b'{"@type": "message", "@principal": "@directory", "@expiry": "1970-01-01T01:00:00+00:00", "@id": "id", "@signature": {"alg": "HS256", "signature": "11c4cc460685c85ac035f3aed98c96ff7a39b6036fa9c81a701ad9c3a3433d76"}}'
        await asyncio.sleep(10000)

    websocket.__aiter__ = receive_messages

    m_uuid = unittest.mock.Mock()
    m_uuid().hex = "64473ce93de046988f93a3feb6e11914"
    monkeypatch.setattr(uuid, "uuid4", m_uuid)

    client = Client("host1", "app", "dummy", "asdf", tmp_path)
    client.start()

    seen_messages: list[JSONObject] = []

    async def handle_message(message: JSONObject) -> None:
        seen_messages.append(message)

    client.register_message_handler("message", handle_message)
    await client.websocket_ready.wait()

    assert websocket.send.call_args_list == [
        unittest.mock.call(
            '{"@type": "aramaki.subscription", "@application": "app", "matches": [{"@type": "message", "scope": {}}], "@context": "https://flyingcircus.io/ns/aramaki", "@version": 1, "@principal": "host1", "@issued": "1970-01-01T00:00:00+00:00", "@expiry": "1970-01-01T01:00:00+00:00", "@id": "64473ce93de046988f93a3feb6e11914", "@signature": {"alg": "HS256", "signature": "58262bcc08f1b6eaa4485c5e7b6da696539426178750e81db20094665ca26e1e"}}'
        )
    ]
    websocket.send.call_args_list = []

    while seen_messages == []:
        await asyncio.sleep(0.1)

    assert seen_messages != []

    await client.send_message("foobar", {"key": "value"})

    calls = websocket.send.call_args_list  # pyright: ignore[reportUnknownMemberType]
    assert calls == [
        unittest.mock.call(
            '{"key": "value", "@type": "foobar", "@context": "https://flyingcircus.io/ns/aramaki", "@version": 1, "@principal": "host1", "@application": "app", "@issued": "1970-01-01T00:00:00+00:00", "@expiry": "1970-01-01T01:00:00+00:00", "@id": "64473ce93de046988f93a3feb6e11914", "@signature": {"alg": "HS256", "signature": "5a97fe6881c6dbe8a73ba95ef63ca1dc2f9882d8494c58b2c6799b13f79e37da"}}'
        ),
    ]
