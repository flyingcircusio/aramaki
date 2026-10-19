import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Protocol

import sqlalchemy
import structlog
from sqlalchemy import JSON, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from aramaki import utils
from aramaki.db import Base
from aramaki.typing import JSONObject

if TYPE_CHECKING:
    from aramaki.client import ClientWithState

log = structlog.stdlib.get_logger()


class Record(Base):
    __tablename__ = "collection_record"

    collection: Mapped[str] = mapped_column(primary_key=True)
    partition: Mapped[str] = mapped_column(primary_key=True)
    record_id: Mapped[str] = mapped_column(primary_key=True)
    version: Mapped[int | None] = mapped_column()
    data: Mapped[JSONObject] = mapped_column(type_=JSON)


async def _currently_known_partition_and_version(
    db_session: AsyncSession, collection: str
) -> tuple[str | None, int]:
    # Use the fact that (collection, partition) is unique for the client view here.
    maybe_result = (
        await db_session.execute(
            select(
                Record.partition,
                func.max(Record.version),
            )
            .filter_by(collection=collection)
            .group_by(Record.partition)
        )
    ).one_or_none()
    if maybe_result is None:
        return None, 0
    partition, max_version = tuple(maybe_result)
    if max_version is None:
        # During a full sync all versions are set to None; treat that as version 0.
        max_version = 0
    return partition, max_version


async def _set_null_record(
    session: AsyncSession, collection: str, partition: str, version: int
) -> None:
    record = await session.get(
        Record,
        {
            "collection": collection,
            "partition": partition,
            "record_id": "",
        },
    )
    if record is None:
        record = Record.create(
            session,
            collection=collection,
            partition=partition,
            record_id="",
            data={},
        )
    record.version = version


class AbstractCollection(Protocol):
    """Protocol defining the read-only collection interface."""

    collection: str

    async def get(
        self,
        key: str,
        default: JSONObject | None = None,
    ) -> JSONObject | None: ...

    async def keys(self) -> list[str]: ...


class Collection:
    """Provides a read-only view to an Aramaki collection.

    The collection provides a simple interface:

        get(key, default=None)
        keys()

    The data is kept (eventually consistent) with the server side, but always available.
    From a CAP perspective, this drops the consistency

    It is updated in the background automatically and automatically detects the need for partial and full syncs.

    """

    collection: str  # The identifier for the collection in Aramaki

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
        self,
        key: str,
        default: JSONObject | None = None,
    ) -> JSONObject | None:
        assert key  # key must be non-empty - defensive against clients breaking protocol that "" is our internal null record
        cursor = await self.session.execute(
            select(Record).filter_by(collection=self.collection, record_id=key)
        )
        result = cursor.scalars().one_or_none()
        if not result:
            return default
        return result.data

    async def keys(self) -> list[str]:
        result = (
            (
                await self.session.execute(
                    select(Record)
                    .filter_by(
                        collection=self.collection,
                    )
                    .filter(Record.record_id != "")
                )
            )
            .scalars()
            .all()
        )
        return [x.record_id for x in result]


class ReplicationManager:
    """Manages the replication for a single collection.

    The replication manager interacts with aramaki by sending and receiving
    replication-related messages.

    We generally buffer messages as we need to ensure proper order (based on the
    versions we receive) when processing them and we need to isolate sync
    activities from regular update activities.

    """

    # TODO This could be improved using a more dynamic timeout that
    # resets whenever we make progress to support longer catchups.
    #
    # seconds to wait for catchup steps before re-requesting
    CATCHUP_TIMEOUT: float = 60

    catchup_running: bool = False
    tasks: set[asyncio.Task[Any]]

    def __init__(
        self,
        aramaki: "ClientWithState",
        collection: type["Collection"],
    ):
        self.collection = collection
        self.aramaki = aramaki
        self.catchup_finished = asyncio.Event()
        self.tasks = set()
        # We have two types of locks here:
        #
        # The update lock to ensure that no update runs concurrently:
        # This is required because we could otherwise get an inconsistent
        # DB state and buffer state, because we delete data in them
        # during catchup.
        self.update_lock = asyncio.Lock()
        # The catchup lock to ensure that all requirements are fulfilled before
        # processing a catchup.step message. This is especially important for
        # the full sync case, as the internal DB (and also the consumer side DB)
        # is wiped.
        self.catchup_lock = asyncio.Lock()

        self.update_buffer = PriorityPushbackQueue()
        self.catchup_buffer = PriorityPushbackQueue()

        self.aramaki.register_message_handler(
            "directory.collection.catchup.start",
            self.process_start_catchup_message,
            principal=self.aramaki.principal,
            application=self.aramaki.application,
            collection=self.collection.collection,
        )
        self.aramaki.register_message_handler(
            "directory.collection.catchup.step",
            self.process_catchup_step_message,
            principal=self.aramaki.principal,
            application=self.aramaki.application,
            collection=self.collection.collection,
        )
        self.aramaki.register_message_handler(
            "directory.collection.update",
            self.process_update_message,
            collection=self.collection.collection,
        )

        for t in [
            self.request_catchup,
            self.process_update_buffer,
            self.process_catchup_step_buffer,
        ]:
            task = utils.create_task(t())
            self.tasks.add(task)

    def stop(self) -> None:
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()

    @asynccontextmanager
    async def get_collection_with_session(
        self,
    ) -> AsyncGenerator[Collection]:
        async with self.aramaki.db.session() as db_session:
            yield self.collection(db_session)

    async def process_update_message(self, msg: dict[str, Any]) -> None:
        log.debug("collection-buffer-update-message", id=msg.get("@id"))
        self.update_buffer.put(msg["version"], msg)

    async def process_update_buffer(self) -> None:
        while True:
            update_version, msg = await self.update_buffer.get()
            # XXX consider switching to pydantic models here
            log.debug(
                "collection-process-update-message",
                id=msg.get("@id"),
                partition=msg["partition"],
                version=update_version,
            )
            if not msg.get("record_id"):
                log.debug(
                    "update-message-broken-protocol",
                    reason="missing field",
                    field="record_id",
                )
                # defensive against peers breaking protocol
                continue
            async with (
                self.update_lock,
                self.aramaki.db.session() as db_session,
            ):
                (
                    current_partition,
                    current_version,
                ) = await _currently_known_partition_and_version(
                    db_session, self.collection.collection
                )

                if current_partition is None or current_partition != msg["partition"]:
                    log.info(
                        "update-message-wrong-partition",
                        current_partition=current_partition,
                        update_partition=msg["partition"],
                        action="catchup",
                    )
                    # There's a certain chance here that, if we get too much of chaotic messages, then we may end up in a flapping
                    # state, e.g. if there's a number of update messages for two partitions (while partitions change) that can cause
                    # (due to version numbers of the new partition being lower) us to early on detect the partition change,
                    # but then find the old partition again in the higher version numbers, this would trigger multiple catchups
                    # but I think this should settle nicely if the upstream partition assignment hasn't changed, so we'd
                    # basically request more catchups but those will quickly converge and not replay everything ...
                    utils.create_task(self.request_catchup())
                    self.update_buffer.task_done()
                    continue

                if update_version <= current_version:
                    log.info(
                        "update-message-old-version",
                        current_version=current_version,
                        update_version=update_version,
                        action="ignore",
                    )
                    # This version is old, ignore it.
                    self.update_buffer.task_done()
                    continue

                if update_version > current_version + 1:
                    log.info(
                        "update-message-skipped-version",
                        current_version=current_version,
                        update_version=update_version,
                        action="put-back",
                    )
                    # This message is too new, keep it in the buffer and wait for another one
                    self.update_buffer.put_back(update_version, msg)
                    continue

                assert update_version == current_version + 1

                record = await db_session.get(
                    Record,
                    {
                        "collection": self.collection.collection,
                        "partition": msg["partition"],
                        "record_id": msg["record_id"],
                    },
                )
                if msg["change"] == "update":
                    if record is None:
                        log.info(
                            "update-message-new-record",
                        )
                        record = Record.create(
                            db_session,
                            collection=self.collection.collection,
                            partition=msg["partition"],
                            record_id=msg["record_id"],
                            version=msg["version"],
                        )
                    else:
                        log.info(
                            "update-message-update-record",
                            partition=msg["partition"],
                            record_id=msg["record_id"],
                            version=msg["version"],
                        )
                    record.version = msg["version"]
                    record.data = msg["data"]
                if msg["change"] == "delete" and record is not None:
                    log.info(
                        "update-message-delete-record",
                        partition=msg["partition"],
                        record_id=msg["record_id"],
                        version=msg["version"],
                    )
                    await record.delete(db_session)
                if msg["change"] == "delete" or msg["change"] == "null":
                    log.info(
                        "update-message-delete-with-null-record",
                        partition=msg["partition"],
                        record_id=msg["record_id"],
                        version=msg["version"],
                    )
                    await _set_null_record(
                        db_session,
                        self.collection.collection,
                        msg["partition"],
                        msg["version"],
                    )
            log.debug(
                "update-message-complete",
                partition=msg["partition"],
                record_id=msg["record_id"],
                version=msg["version"],
            )
            self.update_buffer.task_done()

    async def request_catchup(self) -> None:
        async with self.aramaki.db.session() as db_session:
            (
                current_partition,
                current_version,
            ) = await _currently_known_partition_and_version(
                db_session, self.collection.collection
            )

        log.debug(
            "collection-request-catchup",
            partition=current_partition,
            current_version=current_version,
        )
        await self.aramaki.send_message(
            "directory.collection.catchup.request",
            {
                "collection": self.collection.collection,
                "partition": current_partition,
                "current_version": current_version,
            },
        )

    async def process_start_catchup_message(self, msg: dict[str, Any]) -> None:
        """Start and manage the overall catchup process.

        This can happen in various combinations.

        However, one thing is important: we want to avoid removing records
        too early and delay deletion of records as long as possible to avoid
        flapping for our clients.

        For example:

        - we only mass delete records if the server signals that the partition is empty
        - in partial catchups we only delete those records that we receive deletions for
        - in full catchups we only delete those records that have not received data after the sync

        """
        self.catchup_finished.clear()

        start_version = msg["start_version"]
        partition = msg["partition"]

        log.debug(
            "collection-start-catchup",
            id=msg.get("@id"),
            partition=partition,
            start_version=start_version,
        )

        is_full_sync = False

        # update_lock is held for the entire catchup to block concurrent update
        # message processing. catchup_lock is held only in two narrow phases
        # (stale marking and cleanup) and released during the wait so that
        # process_catchup_step_buffer (which also acquires catchup_lock per step)
        # can proceed without deadlocking.
        async with self.update_lock:
            async with (
                self.catchup_lock,
                self.aramaki.db.session() as db_session,
            ):
                current_partition = (
                    await _currently_known_partition_and_version(
                        db_session, self.collection.collection
                    )
                )[0]

                if start_version == 0:
                    # The partition is empty and we will not receive further messages.
                    await db_session.execute(
                        sqlalchemy.delete(Record).filter_by(
                            collection=self.collection.collection
                        )
                    )
                    await _set_null_record(
                        db_session, self.collection.collection, partition, 0
                    )
                    return

                if partition != current_partition and start_version > 1:
                    # We switched partitions but that means we can't do a partial sync.
                    # Re-request a full sync (not re-using request_catchup because
                    # we don't want to use the persistent data we have).
                    log.debug(
                        "collection-request-catchup",
                        partition=partition,
                        current_version=0,
                    )
                    await self.aramaki.send_message(
                        "directory.collection.catchup.request",
                        {
                            "collection": self.collection.collection,
                            "partition": partition,
                            "current_version": 0,
                        },
                    )
                    return

                if is_full_sync := start_version == 1:
                    log.debug(
                        "collection-full-sync",
                        status="start",
                        partition=partition,
                        current_version=0,
                    )
                    # Mark all existing records as stale (version=None). Catchup
                    # steps restore proper versions; any record still None after
                    # the sync is deleted below. Holding catchup_lock here makes
                    # this marking atomic with respect to step processing.
                    await db_session.execute(
                        sqlalchemy.update(Record)
                        .filter_by(collection=self.collection.collection)
                        .values(version=None)
                    )
            # Let the sync continue (we dropped the catchup lock)
            try:
                log.error("waiting for timeout", timeout=self.CATCHUP_TIMEOUT)
                await asyncio.wait_for(
                    self.catchup_finished.wait(), timeout=self.CATCHUP_TIMEOUT
                )
            except TimeoutError:
                log.error(
                    "collection-catchup-timeout",
                    partition=partition,
                    start_version=start_version,
                )
                utils.create_task(self.request_catchup())
                return

            if is_full_sync:
                log.debug("collection-full-sync", status="finished")
                async with (
                    self.catchup_lock,
                    self.aramaki.db.session() as db_session,
                ):
                    # Delete all items that haven't received version markers during the catchup.
                    await db_session.execute(
                        sqlalchemy.delete(Record).filter_by(
                            collection=self.collection.collection,
                            version=None,
                        )
                    )

    async def process_catchup_step_message(self, msg: dict[str, Any]) -> None:
        self.catchup_buffer.put(msg["from_version"], msg)

    async def process_catchup_step_buffer(self) -> None:
        while True:
            from_version, msg = await self.catchup_buffer.get()
            log.debug(
                "collection-process-catchup-step-buffer",
                id=msg.get("@id"),
                from_version=from_version,
                to_version=msg["to_version"],
                change=msg["change"],
            )
            async with (
                self.catchup_lock,
                self.aramaki.db.session() as db_session,
            ):
                current_version = (
                    await _currently_known_partition_and_version(
                        db_session, self.collection.collection
                    )
                )[1]
                if msg["from_version"] < current_version:
                    # Discard the message, we already processed a newer one
                    self.catchup_buffer.task_done()
                    continue
                if msg["from_version"] > current_version:
                    # This message is too new, keep it in the buffer and wait for another one
                    self.catchup_buffer.put_back(from_version, msg)
                    continue

                record = await db_session.get(
                    Record,
                    {
                        "collection": self.collection.collection,
                        "partition": msg["partition"],
                        "record_id": msg.get("record_id"),
                    },
                )
                if msg["change"] == "update":
                    if record is None:
                        record = Record.create(
                            db_session,
                            collection=self.collection.collection,
                            partition=msg["partition"],
                            record_id=msg["record_id"],
                        )

                    record.version = msg["to_version"]
                    record.data = msg["data"]

                if msg["change"] == "delete" and record is not None:
                    await record.delete(db_session)

                if msg["change"] == "delete" or msg["change"] == "null":
                    await _set_null_record(
                        db_session,
                        self.collection.collection,
                        msg["partition"],
                        msg["to_version"],
                    )
            # After commit (catchup_lock released)
            if msg.get("is_final_record"):
                self.catchup_finished.set()
            self.catchup_buffer.task_done()


class PriorityPushbackQueue:
    """A priority queue that allows putting items back.

    It also supports non-hashable objects.

    Putting an item back means we do not pass it out to waiters
    until at least one another item with a lower priority
    has been put in.

    Typically inversed priority meaning: a lower number indicates a higher priority.

    """

    metric_put_back: int = 0
    items: dict[int, list[Any]]
    queue: asyncio.PriorityQueue[int]
    last_put_back: int | None = None

    def __init__(self) -> None:
        self.items = {}
        self.queue = asyncio.PriorityQueue()
        self.new_item = asyncio.Event()

    def put(self, priority: int, item: Any) -> None:
        self.items.setdefault(priority, []).append(item)
        self.queue.put_nowait(priority)
        # Only signal new items if we haven't put anything back
        # or got a higher priority since the last putback
        if self.last_put_back and priority >= self.last_put_back:
            return
        self.last_put_back = None
        self.new_item.set()

    def put_back(self, priority: int, item: Any) -> None:
        self.metric_put_back += 1
        self.items.setdefault(priority, []).append(item)
        if self.queue.empty() or self.queue._queue[0] >= priority:  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            # If other items can in they must be of higher priority
            # to allow immediately passing through without waiting
            # for new items. There is a bit of further optimization
            # possible if we'd keep track of the last priority that was
            # put back and then not setting
            self.new_item.clear()
            self.last_put_back = priority
        self.queue.put_nowait(priority)
        # The client should not mark this as "task done", we do that for it.
        self.queue.task_done()

    async def get(self) -> tuple[int, Any]:
        await self.new_item.wait()
        priority = self.queue.get_nowait()
        if self.queue.empty():
            self.new_item.clear()
        return priority, self.items[priority].pop(0)

    async def join(self) -> None:
        await self.queue.join()

    def task_done(self) -> None:
        self.queue.task_done()
