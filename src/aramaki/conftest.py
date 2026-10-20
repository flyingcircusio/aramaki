import datetime
import time
import unittest
from collections.abc import Generator

import pytest


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
