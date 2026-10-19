import contextlib
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any, Protocol, Self

import structlog.stdlib
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

DBSession = AsyncSession  # Alias for easier referencing
log = structlog.stdlib.get_logger()


class SessionManagerClosed(Exception):
    pass


class DBSessionManager(Protocol):
    def session(self) -> contextlib.AbstractAsyncContextManager[AsyncSession]: ...


class Base(DeclarativeBase):
    @classmethod
    def create(cls, session: AsyncSession, **kwargs: Any) -> Self:
        obj = cls(**kwargs)
        session.add(obj)
        return obj

    async def delete(self, db: AsyncSession) -> None:
        await db.delete(self)


class SqliteDBSessionManager(DBSessionManager):
    state_directory: Path

    def __init__(self, state_directory: Path):
        self.state_directory = state_directory
        db_url = f"sqlite+aiosqlite:///{self.state_directory!s}/aramaki.sqlite3"
        self._engine = create_async_engine(db_url)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False
        )

    def upgrade(self) -> None:
        log.info("Upgrading aramaki database")
        config = Config()
        db_url = f"sqlite:///{self.state_directory!s}/aramaki.sqlite3"
        from sqlalchemy import create_engine

        config.set_main_option("script_location", "aramaki:alembic")
        config.set_main_option("sqlalchemy.url", db_url)
        engine = create_engine(db_url)
        with engine.connect() as connection:
            config.attributes["connection"] = connection
            command.upgrade(config, "head")

    async def close(self):
        if self._engine is None:
            return
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession]:
        if self._sessionmaker is None:
            raise SessionManagerClosed()

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        else:
            await session.commit()
        finally:
            await session.close()
