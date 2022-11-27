import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .meta import AbstractApplicationContext


class URLDescriptor:
    def __init__(self, pattern):
        self.pattern = pattern

    def __get__(self, obj, objtype=None):
        return urllib.parse.urljoin(
            context.application_url, self.pattern.format(**obj.__dict__)
        )


class Context(AbstractApplicationContext):
    """External context that a domain model needs to actually function
    within the real world.

    "The domain model may only interact with the real world by accessing
    the context."

    The context provides the domain model with abstract dependencies during
    import time and fills in specific implementations to access during runtime.

    Based on the concepts from Cosmic Python, this is a combination of:

    * Unit of Work (we only support SQLAlchemy, this is not pluggable)
      * transaction management
    * Message Bus (event handling)
    * Bootstrapping
    * Config
    * Dependency Injection

    classmethods can be used during import time in the Domain model
    (like `context.handle` to register event handlers)

    During runtime you can access methods like `context.event` to trigger events.


    """

    def bind(self, db_uri, application_url):
        self.db_uri = db_uri
        self.application_url = application_url

        # Import all model modules, to ensure SQLAlchemy
        # picks them up. Potentially use scanning here.
        # XXX consider scanning here
        import aramaki.activitypub
        import aramaki.interfaces.activitypub
        import aramaki.notification
        import aramaki.system

        self.session_factory = sessionmaker(
            bind=create_engine(self.db_uri, echo=False, future=True)
        )

        self.activitypub = (
            aramaki.interfaces.activitypub.InternalActivityPubRouter(self)
        )

    def enter(self):
        self.session = self.session_factory()

    def exit(self, *args):
        self.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @classmethod
    def url(cls, pattern):
        return URLDescriptor(pattern)


context = Context.setup()
