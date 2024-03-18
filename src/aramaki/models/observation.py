import uuid
from typing import Any

from sqlalchemy import ForeignKey, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import meta
from .system import System


class Observation(meta.Base):
    """Observations"""

    __tablename__ = "observation"

    system_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("system.id"), init=False, primary_key=True
    )
    system: Mapped[System] = relationship(System)

    name: Mapped[str] = mapped_column(primary_key=True)

    # labels are expected to be of the form
    # key=value,key=value and in order to ensure the primary
    # key property
    labels: Mapped[str] = mapped_column(primary_key=True)

    # XXX mutability tracking
    data: Mapped[dict[str, Any]]

    # XXX mutability tracking
    # tags: Mapped[set[str]]

    @classmethod
    def record(cls, uow, system_id, name, data, labels=""):
        # XXX this is a performance killer, but the dataclass
        # approach doesn't allow me to add a system_id
        system = uow.session.execute(
            select(System).filter_by(id=system_id)
        ).scalar_one()
        try:
            observation = uow.session.execute(
                select(Observation).filter_by(
                    system=system, name="ping", labels=""
                )
            ).scalar_one()
            observation.data = data
        except NoResultFound:
            observation = Observation(
                system=system, name="ping", labels="", data=data, tags=set()
            )
            uow.session.add(observation)

        uow.events.append(observation)
        return observation

    def tag(self, uow, tag):
        if tag in self.tags:
            return
        self.tags |= {tag}
        # XXX passing the UoW around here feels wrong
        uow.events.append(self)

    def untag(self, uow, tag):
        if tag not in self.tags:
            return
        self.tags -= {tag}
        uow.events.append(self)
