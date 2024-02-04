import uuid

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship

from . import meta

subsystem = Table(
    "subsystem",
    meta.Base.metadata,
    Column("system_id", ForeignKey("system.id"), primary_key=True),
    Column("subsystem_id", ForeignKey("system.id"), primary_key=True),
)


class System(meta.UIDBase):
    __tablename__ = "system"

    # Make this a dictionary, use references
    type_: Mapped[str]

    # XXX Turn into relationship
    primary_instance: Mapped[uuid.UUID]

    title: Mapped[str]

    # Subsystems are designed specifically as an n-to-m relation ship with the
    # idea that the subsystems itself should be quite independent and that this
    # is an organizational relationship for the UI that should be flexible.
    #
    # To avoid too many implicit dependencies on attributes from the parents
    # I'm currently not setting up the inverse relationship. We'll see how
    # this goes and whether this can hold over time.
    subsystems: Mapped[list["System"]] = relationship(
        secondary=subsystem,
        primaryjoin="system.c.id == subsystem.c.system_id",
        secondaryjoin="system.c.id == subsystem.c.subsystem_id",
        default_factory=list,
    )
