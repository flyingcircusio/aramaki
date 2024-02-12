import os

import alembic
import alembic.command
import alembic.config
import pytest
import transaction
import zope.testbrowser.wsgi
from pyramid.paster import get_appsettings

from aramaki.server import models
from aramaki.server.models.meta import Base
from aramaki.server.web.main import main


def pytest_addoption(parser):
    parser.addoption("--ini", action="store", metavar="INI_FILE")


@pytest.fixture(scope="session")
def ini_file(request):
    # potentially grab this path from a pytest option
    return os.path.abspath(request.config.getoption("--ini", "testing.ini"))


@pytest.fixture(scope="session")
def app_settings(ini_file):
    return get_appsettings(ini_file)


@pytest.fixture
def dbengine(app_settings, ini_file):
    engine = models.get_engine(app_settings)

    alembic_cfg = alembic.config.Config(ini_file)
    Base.metadata.drop_all(bind=engine)
    # https://github.com/sqlalchemy/alembic/issues/1420
    alembic.command.stamp(alembic_cfg, None, purge=True)  # type: ignore

    alembic.command.upgrade(alembic_cfg, "head")

    yield engine


@pytest.fixture
def app(app_settings, dbengine):
    return main({}, dbengine=dbengine, **app_settings)


@pytest.fixture
def dbsession(app):
    session_factory = app.registry["dbsession_factory"]
    with transaction.manager:
        yield models.get_tm_session(session_factory, transaction.manager)


@pytest.fixture
def testbrowser(app):
    """A fully functional testbrowser stack.

    This uses a fully functional database integration and thus requires
    test database support to replace the database cleanly after each test.

    """
    return zope.testbrowser.wsgi.Browser(wsgi_app=app)
