import pytest

from aramaki import context


def make_context(name, tmp_path):
    c = context.bind(
        application_url=f"http://{name}.example.net/",
        db_uri=f"sqlite:////{tmp_path}/{name}.sqlite",
    )
    from aramaki.interfaces.sqlalchemy import Base

    with c:
        Base.metadata.create_all(c.session.bind)
    return c


@pytest.fixture
def fcio(tmp_path):
    yield make_context("fcio", tmp_path)


@pytest.fixture
def customer(tmp_path):
    yield make_context("customer", tmp_path)
