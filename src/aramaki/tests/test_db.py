from pathlib import Path

import pytest

from aramaki.db import DBSessionManager, SessionManagerClosed, SqliteDBSessionManager


async def test_session_manager(tmp_path: Path):
    manager = SqliteDBSessionManager(tmp_path)
    manager.upgrade()

    assert manager._engine is not None  # pyright: ignore[reportPrivateUsage]
    sm = manager._sessionmaker  # pyright: ignore[reportPrivateUsage]
    assert sm is not None

    await manager.close()

    assert manager._engine is None  # pyright: ignore[reportPrivateUsage]
    sm = manager._sessionmaker  # pyright: ignore[reportPrivateUsage]
    assert sm is None

    # idempotent

    await manager.close()

    assert manager._engine is None  # pyright: ignore[reportPrivateUsage]
    sm = manager._sessionmaker  # pyright: ignore[reportPrivateUsage]
    assert sm is None


async def test_session_manager_context_manager(tmp_path: Path):
    manager = SqliteDBSessionManager(tmp_path)
    manager.upgrade()

    async with manager.session():
        pass

    class CustomError(Exception):
        pass

    with pytest.raises(CustomError):
        async with manager.session():
            raise CustomError()

    await manager.close()

    with pytest.raises(SessionManagerClosed):
        async with manager.session():
            pass
