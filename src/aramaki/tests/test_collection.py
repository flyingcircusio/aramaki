import asyncio
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import pytest

import aramaki
import aramaki.collection
import aramaki.db


class DummyCollection(aramaki.Collection):
    collection = "mydummycollection"


async def test_collection_basics(tmp_path: Path):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    async with db.session() as session:
        collection = DummyCollection(session)

        assert (
            await aramaki.collection._currently_known_partition_and_version(  # pyright: ignore[reportPrivateUsage]
                session, collection.collection
            )
        ) == (
            None,
            0,
        )

        assert await collection.get("test") is None
        assert await collection.keys() == []

        item = aramaki.collection.Record(
            collection="mydummycollection",
            partition="x",
            record_id="test",
            data={},
            version=1,
        )
        session.add(item)

        assert await collection.get("test") == {}
        assert await collection.keys() == ["test"]

        assert (
            await aramaki.collection._currently_known_partition_and_version(  # pyright: ignore[reportPrivateUsage]
                session, collection.collection
            )
        ) == (
            "x",
            1,
        )

        assert await collection.get("foobar") is None
        assert await collection.get("foobar", {"value": 5}) == {"value": 5}


async def test_null_record(tmp_path: Path):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    async with db.session() as session:
        collection = DummyCollection(session)

        with pytest.raises(AssertionError):
            await collection.get("")

        assert (
            await session.get(
                aramaki.collection.Record,
                {
                    "collection": "collection-1",
                    "partition": "partition-1",
                    "record_id": "",
                },
            )
        ) is None

        await aramaki.collection._set_null_record(  # pyright: ignore[reportPrivateUsage]
            session, "collection-1", "partition-1", 10
        )

        record_10 = await session.get(
            aramaki.collection.Record,
            {
                "collection": "collection-1",
                "partition": "partition-1",
                "record_id": "",
            },
        )
        assert record_10 is not None
        assert record_10.version == 10

        await aramaki.collection._set_null_record(  # pyright: ignore[reportPrivateUsage]
            session, "collection-1", "partition-1", 20
        )

        record_20 = await session.get(
            aramaki.collection.Record,
            {
                "collection": "collection-1",
                "partition": "partition-1",
                "record_id": "",
            },
        )
        assert record_20 is not None
        assert record_20.version == 20


async def test_pushback_queue():
    queue = aramaki.collection.PriorityPushbackQueue()
    queue.put(3, "3")
    queue.put(1, "1")
    queue.put(2, "2")
    assert await queue.get() == (1, "1")
    assert await queue.get() == (2, "2")
    assert await queue.get() == (3, "3")

    queue.put(3, "3")
    queue.put(2, "2")
    assert await queue.get() == (2, "2")
    queue.put_back(2, "2")

    task = asyncio.create_task(queue.get())
    await asyncio.sleep(0.1)
    assert not task.done()
    queue.put(1, "1")
    await task
    assert task.result() == (1, "1")
    assert await queue.get() == (2, "2")
    assert await queue.get() == (3, "3")


async def test_pushback_queue_race_condition():
    queue = aramaki.collection.PriorityPushbackQueue()
    queue.put(2, "item 2")
    p, _ = await queue.get()
    assert p == 2
    queue.put(1, "item 1")
    queue.put_back(2, "item 2")
    p, _ = await asyncio.wait_for(queue.get(), timeout=10.0)
    assert p == 1


async def test_pushback_queue_put_high_priority_after_put_back():
    queue = aramaki.collection.PriorityPushbackQueue()

    queue.put(5, "item-5")
    await queue.get()

    queue.put_back(5, "item-5")
    assert not queue.new_item.is_set()

    # Same-or-lower priority (higher number) after put_back: new_item stays clear
    queue.put(7, "item-7")
    assert not queue.new_item.is_set()

    # Higher priority (lower number) clears last_put_back and wakes up waiters
    queue.put(3, "item-3")
    assert queue.new_item.is_set()

    assert await queue.get() == (3, "item-3")
    assert await queue.get() == (5, "item-5")
    assert await queue.get() == (7, "item-7")

    assert not queue.new_item.is_set()


class AramakiDummy:
    principal = "host1"
    application = "test"

    db: aramaki.db.DBSessionManager
    message: tuple[tuple[Any, ...], dict[str, Any]] | None

    def __init__(self):
        self.message_received = asyncio.Event()

    def register_message_handler(
        self,
        type_: str,
        callback: Callable[[dict[str, Any]], Awaitable[Any]],
        **scope: str,
    ) -> None:
        pass

    async def send_message(self, *args: Any, **kw: Any) -> None:
        self.message = args, kw
        self.message_received.set()


async def test_replication(tmp_path: Path):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with manager.get_collection_with_session() as collection:
        await aramaki_manager.message_received.wait()
        assert aramaki_manager.message == (
            (
                "directory.collection.catchup.request",
                {
                    "collection": "mydummycollection",
                    "current_version": 0,
                    "partition": None,
                },
            ),
            {},
        )
        # let's run through a full sync
        assert await collection.get("1") is None
        catchup_task = asyncio.create_task(
            manager.process_start_catchup_message(
                {"start_version": 1, "partition": "partition-1"}
            )
        )
        await manager.process_catchup_step_message(
            {
                "from_version": 0,
                "record_id": "1",
                "partition": "partition-1",
                "to_version": 1,
                "change": "update",
                "is_final_record": False,
                "data": {"key": "value"},
            }
        )
        await manager.process_catchup_step_message(
            {
                "from_version": 1,
                "record_id": "1",
                "partition": "partition-1",
                "to_version": 2,
                "change": "update",
                "is_final_record": True,
                "data": {"key": "value"},
            }
        )
        await catchup_task
        assert await collection.get("1") == {"key": "value"}

        # now lets run some updates
        await manager.process_update_message(
            {
                "record_id": "1",
                "partition": "partition-1",
                "version": 3,
                "change": "update",
                "data": {"key": "other-value"},
            }
        )

        await manager.update_buffer.join()

        assert await collection.get("1") == {"key": "other-value"}

        await manager.process_update_message(
            {
                "record_id": "1",
                "partition": "partition-1",
                "version": 4,
                "change": "delete",
            }
        )

        await manager.update_buffer.join()

        assert await collection.get("1") is None

        # This is an outdated version
        await manager.process_update_message(
            {
                "record_id": "1",
                "partition": "partition-1",
                "version": 2,
                "change": "update",
                "data": {"key": "other-value"},
            }
        )
        await manager.process_update_message(
            {
                "record_id": "1",
                "partition": "partition-1",
                "version": 3,
                "change": "update",
                "data": {"key": "other-value"},
            }
        )

        await manager.update_buffer.join()

        assert await collection.get("1") is None

        # This is too new
        await manager.process_update_message(
            {
                "record_id": "1",
                "partition": "partition-1",
                "version": 6,
                "change": "update",
                "data": {"key": "value-6"},
            }
        )

        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(manager.update_buffer.join(), timeout=0.1)

        assert await collection.get("1") is None

        # This is the right next version and we then
        # catch up to version 5 immediately.
        await manager.process_update_message(
            {
                "record_id": "2",
                "partition": "partition-1",
                "version": 5,
                "change": "update",
                "data": {"key": "value-5"},
            }
        )

        await manager.update_buffer.join()

        assert await collection.get("1") == {"key": "value-6"}
        assert await collection.get("2") == {"key": "value-5"}

    manager.stop()


async def test_full_sync_race_step_blocked_during_marking(
    tmp_path: Path,
):
    """
    Regression for the intermittent race described in the original failure log:

        collection-process-catchup-step-buffer from_version=0 to_version=1   ← step committed first
        collection-full-sync           status=start                          ← then marking tried UPDATE SET version=NULL
        NOT NULL constraint failed: collection_record.version

    Reproduced deterministically: pre-insert a record so that
    process_start_catchup_message's UPDATE SET version=NULL immediately hits
    NOT NULL constraint on unfixed code (version: Mapped[int]).  With the fix
    (version: Mapped[int | None] and catchup_lock protecting both marking and
    each step) the UPDATE succeeds and the step is processed after marking,
    leaving the record intact.
    """
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with manager.get_collection_with_session() as collection:
        await aramaki_manager.message_received.wait()

        # Pre-insert a record to simulate a step having committed before the
        # marking phase runs — this is what caused the intermittent crash.
        async with db.session() as session:
            aramaki.collection.Record.create(
                session,
                collection=DummyCollection.collection,
                partition="partition-1",
                record_id="1",
                version=1,
                data={"key": "old"},
            )

        catchup_task = asyncio.create_task(
            manager.process_start_catchup_message(
                {"start_version": 1, "partition": "partition-1"}
            )
        )
        await manager.process_catchup_step_message(
            {
                "from_version": 0,
                "record_id": "1",
                "partition": "partition-1",
                "to_version": 1,
                "change": "update",
                "is_final_record": False,
                "data": {"key": "value"},
            }
        )
        await manager.process_catchup_step_message(
            {
                "from_version": 1,
                "record_id": "1",
                "partition": "partition-1",
                "to_version": 2,
                "change": "update",
                "is_final_record": True,
                "data": {"key": "value"},
            }
        )

        manager.CATCHUP_TIMEOUT = 5
        await catchup_task

        assert await collection.get("1") == {"key": "value"}

    manager.stop()


async def test_replication_empty_sync(tmp_path: Path):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    await aramaki_manager.message_received.wait()
    assert aramaki_manager.message == (
        (
            "directory.collection.catchup.request",
            {
                "collection": "mydummycollection",
                "current_version": 0,
                "partition": None,
            },
        ),
        {},
    )
    async with manager.get_collection_with_session() as collection:
        # let's run through a full sync
        assert await collection.keys() == []

        await manager.process_start_catchup_message(
            {"start_version": 0, "partition": "partition-1"}
        )

        assert await collection.keys() == []

        await manager.process_update_message(
            {
                "record_id": "1",
                "partition": "partition-1",
                "version": 1,
                "change": "update",
                "data": {"key": "other-value"},
            }
        )

        await asyncio.wait_for(manager.update_buffer.join(), timeout=1)

        assert await collection.keys() == ["1"]

        await manager.process_start_catchup_message(
            {"start_version": 0, "partition": "partition-1"}
        )

        assert await collection.keys() == []


async def test_replication_catchup_sync(tmp_path: Path):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    async with db.session() as session:
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="1",
            version=4,
            data={},
        )
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="2",
            version=5,
            data={},
        )

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with manager.get_collection_with_session() as collection:
        await aramaki_manager.message_received.wait()

        assert aramaki_manager.message == (
            (
                "directory.collection.catchup.request",
                {
                    "collection": "mydummycollection",
                    "current_version": 5,
                    "partition": "partition-1",
                },
            ),
            {},
        )

        # let's run through a partial sync
        catchup_task = asyncio.create_task(
            manager.process_start_catchup_message(
                {"start_version": 6, "partition": "partition-1"}
            )
        )
        await manager.process_catchup_step_message(
            {
                "from_version": 5,
                "record_id": "1",
                "partition": "partition-1",
                "to_version": 6,
                "change": "delete",
            }
        )
        await manager.process_catchup_step_message(
            {
                "from_version": 6,
                "record_id": "2",
                "partition": "partition-1",
                "to_version": 10,
                "change": "update",
                "data": {"key": "value-10"},
                "is_final_record": True,
            }
        )

        await catchup_task

        assert await collection.get("1") is None
        assert await collection.get("2") == {"key": "value-10"}


async def test_catchup_step_discards_stale_message(tmp_path: Path):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    async with db.session() as session:
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="1",
            version=5,
            data={"key": "current"},
        )

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with manager.get_collection_with_session() as collection:
        # from_version=3 < current_version=5: the step should be discarded
        await manager.process_catchup_step_message(
            {
                "from_version": 3,
                "record_id": "1",
                "partition": "partition-1",
                "to_version": 4,
                "change": "update",
                "is_final_record": False,
                "data": {"key": "stale"},
            }
        )

        await manager.catchup_buffer.join()

        assert await collection.get("1") == {"key": "current"}

    manager.stop()


async def test_catchup_timeout_releases_lock_and_rerequests(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """If the server never sends is_final_record, the lock must not be held forever."""
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    async with db.session() as session:
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="1",
            version=5,
            data={},
        )

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    manager.CATCHUP_TIMEOUT = 0.05

    async with manager.get_collection_with_session():
        await aramaki_manager.message_received.wait()
        aramaki_manager.message_received.clear()
        aramaki_manager.message = None

        # Start catchup — server never sends is_final_record, catchup_finished never set
        catchup_task = asyncio.create_task(
            manager.process_start_catchup_message(
                {"start_version": 6, "partition": "partition-1"}
            )
        )

        # Timeout fires, re-requests catchup, releases update_lock
        await asyncio.wait_for(aramaki_manager.message_received.wait(), timeout=2)

        assert catchup_task.done()
        assert aramaki_manager.message is not None
        assert aramaki_manager.message[0][0] == "directory.collection.catchup.request"

        # update_lock must be released — update_buffer can drain without deadlocking
        await manager.process_update_message(
            {
                "record_id": "1",
                "partition": "partition-1",
                "version": 1,
                "change": "update",
                "data": {"key": "value"},
            }
        )
        # The update triggers another catchup (unknown partition), but the point
        # is that update_buffer.join() completes — the lock is no longer held.
        await asyncio.wait_for(manager.update_buffer.join(), timeout=1)

    manager.stop()


async def test_full_sync_deletes_superfluous_records_at_end(
    tmp_path: Path,
):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    async with db.session() as session:
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="1",
            version=4,
            data={},
        )
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="2",
            version=5,
            data={},
        )

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with manager.get_collection_with_session() as collection:
        await aramaki_manager.message_received.wait()

        assert aramaki_manager.message == (
            (
                "directory.collection.catchup.request",
                {
                    "collection": "mydummycollection",
                    "current_version": 5,
                    "partition": "partition-1",
                },
            ),
            {},
        )

        # let's run through a partial sync
        catchup_task = asyncio.create_task(
            manager.process_start_catchup_message(
                {"start_version": 0, "partition": "partition-1"}
            )
        )
        assert await collection.keys() == ["1", "2"]
        await manager.process_catchup_step_message(
            {
                "from_version": 0,
                "record_id": "1",
                "partition": "partition-1",
                "to_version": 1,
                "change": "null",
                "is_final_record": True,
            }
        )
        await catchup_task
        assert await collection.keys() == []


async def test_update_with_missing_partition_triggers_catchup(
    tmp_path: Path,
):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with manager.get_collection_with_session() as collection:
        await aramaki_manager.message_received.wait()
        aramaki_manager.message = None

        assert await collection.keys() == []
        # Send an update message -> triggers a catchup

        await manager.process_update_message(
            {
                "record_id": "1",
                "partition": "partition-1",
                "version": 5,
                "change": "update",
                "data": {"key": "other-value"},
            }
        )

        await manager.update_buffer.join()

        assert await collection.keys() == []

        while aramaki_manager.message is None:
            await asyncio.sleep(0.1)

        assert aramaki_manager.message == (
            (
                "directory.collection.catchup.request",
                {
                    "collection": "mydummycollection",
                    "current_version": 0,
                    "partition": None,
                },
            ),
            {},
        )


async def test_update_with_wrong_partition_triggers_catchup(
    tmp_path: Path,
):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with db.session() as session:
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="1",
            version=4,
            data={},
        )

    async with manager.get_collection_with_session() as collection:
        await aramaki_manager.message_received.wait()
        aramaki_manager.message = None

        assert await collection.keys() == ["1"]

        # Send an update message -> triggers a catchup
        await manager.process_update_message(
            {
                "record_id": "5",
                "partition": "partition-2",
                "version": 5,
                "change": "update",
                "data": {"key": "other-value"},
            }
        )

        await manager.update_buffer.join()

        assert await collection.keys() == ["1"]
        while aramaki_manager.message is None:
            await asyncio.sleep(0.1)

        assert aramaki_manager.message == (
            (
                "directory.collection.catchup.request",
                {
                    "collection": "mydummycollection",
                    "current_version": 4,
                    "partition": "partition-1",
                },
            ),
            {},
        )


async def test_partial_sync_wrong_partition_restart_catchup(
    tmp_path: Path,
):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    async with db.session() as session:
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="1",
            version=4,
            data={},
        )

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with manager.get_collection_with_session() as collection:
        await aramaki_manager.message_received.wait()
        assert aramaki_manager.message == (
            (
                "directory.collection.catchup.request",
                {
                    "collection": "mydummycollection",
                    "current_version": 4,
                    "partition": "partition-1",
                },
            ),
            {},
        )
        aramaki_manager.message = None

        assert await collection.keys() == ["1"]

        # Get a partial catchup initiation but with the wrong partition -> request a new full sync
        catchup_task = asyncio.create_task(
            manager.process_start_catchup_message(
                {"start_version": 2, "partition": "partition-2"}
            )
        )
        assert await collection.keys() == ["1"]
        await catchup_task

        assert await collection.keys() == ["1"]
        assert aramaki_manager.message == (
            (
                "directory.collection.catchup.request",
                {
                    "collection": "mydummycollection",
                    "current_version": 0,
                    "partition": "partition-2",
                },
            ),
            {},
        )


async def test_replication_catchup_out_of_order(tmp_path: Path):
    db = aramaki.db.SqliteDBSessionManager(tmp_path)
    db.upgrade()

    aramaki_manager = AramakiDummy()
    aramaki_manager.db = db

    async with db.session() as session:
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="1",
            version=4,
            data={},
        )
        aramaki.collection.Record.create(
            session,
            collection="mydummycollection",
            partition="partition-1",
            record_id="2",
            version=5,
            data={},
        )

    manager = aramaki.collection.ReplicationManager(
        aramaki_manager,  # pyright: ignore[reportArgumentType]
        DummyCollection,
    )

    async with manager.get_collection_with_session() as collection:
        await aramaki_manager.message_received.wait()

        assert aramaki_manager.message == (
            (
                "directory.collection.catchup.request",
                {
                    "collection": "mydummycollection",
                    "current_version": 5,
                    "partition": "partition-1",
                },
            ),
            {},
        )

        # let's run through a partial sync
        catchup_task = asyncio.create_task(
            manager.process_start_catchup_message(
                {"start_version": 6, "partition": "partition-1"}
            )
        )
        await manager.process_catchup_step_message(
            {
                "from_version": 6,
                "record_id": "2",
                "partition": "partition-1",
                "to_version": 10,
                "change": "update",
                "data": {"key": "value-10"},
                "is_final_record": True,
            }
        )

        while manager.catchup_buffer.metric_put_back == 0:
            await asyncio.sleep(0.1)

        await manager.process_catchup_step_message(
            {
                "from_version": 5,
                "record_id": "1",
                "partition": "partition-1",
                "to_version": 6,
                "change": "delete",
            }
        )

        await catchup_task

        assert await collection.get("1") is None
        assert await collection.get("2") == {"key": "value-10"}
