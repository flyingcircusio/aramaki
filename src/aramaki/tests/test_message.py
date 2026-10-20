import unittest.mock
import uuid

import pytest

from aramaki.message import Message


async def test_create_message_defaults(
    now: unittest.mock.Mock, monkeypatch: pytest.MonkeyPatch
):
    m_uuid = unittest.mock.Mock()
    m_uuid().hex = "64473ce93de046988f93a3feb6e11914"
    monkeypatch.setattr(uuid, "uuid4", m_uuid)
    message = Message(
        key="value", principal="host1", application="app", type="aramaki.tests"
    )
    message.sign("asdf".encode("ascii"))

    message = message.model_dump(mode="json")
    assert message == {
        "key": "value",
        "@id": "64473ce93de046988f93a3feb6e11914",
        "@type": "aramaki.tests",
        "@context": "https://flyingcircus.io/ns/aramaki",
        "@version": 1,
        "@principal": "host1",
        "@application": "app",
        "@issued": "1970-01-01T00:00:00+00:00",
        "@expiry": "1970-01-01T01:00:00+00:00",
        "@signature": {
            "alg": "HS256",
            "signature": "ef24b7e55264b3aa7f9d46d9e46582256e673f82c58fb03f2c779759c0f3109d",
        },
    }
