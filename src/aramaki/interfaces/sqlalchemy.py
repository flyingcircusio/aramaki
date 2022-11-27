from sqlalchemy.orm import declarative_base

import aramaki.activitypub
from aramaki import context

# declarative base class
AbstractBase = declarative_base()


def ensure_actor_id(something):
    if isinstance(something, Base):
        return something.actor_id
    return something


class Base(AbstractBase):

    __abstract__ = True

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        context.session.add(obj)
        return obj

    @classmethod
    def list(cls):
        return context.session.query(cls).all()

    @classmethod
    def get(cls, **kw):
        return context.session.query(cls).filter_by(**kw).one()

    # XXX this isn't sqlalchemy but activitypub
    def publish(self, type, object, to=None):
        object = ensure_actor_id(object)
        if not to:
            to = object
        else:
            to = ensure_actor_id(to)

        if not to:
            to = object
        if isinstance(to, Base):
            # XXX
            pass

    def respond(self, type, object):
        pass
