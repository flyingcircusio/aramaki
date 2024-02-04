import uuid

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import meta

subsystem = Table(
    "subsystem",
    meta.Base.metadata,
    Column("system_id", ForeignKey("system.id"), primary_key=True),
    Column("subsystem_id", ForeignKey("system.id"), primary_key=True),
)


class SystemCategory(meta.UIDBase):
    """Specify the an abstract system's category."""

    __tablename__ = "system_category"

    title: Mapped[str]


class System(meta.UIDBase):
    """Systems are the main unit of granularity in Aramaki.

    They represent something that is being managed in the "DevOps control
    plane" sense.

    Systems belong to specific categories and we usually do not reference
    the term "system" in too many places, but we rather want to fit into
    whatever vernacular is present in teams already.

    Thus, systems have a type and then we talk about that:

    * If the type is "infrastructure" we talk about the "storage
      infrastructure" instead of "the storage system".

    * If the type is a "service" we talk about the "Wiki service" instead of
      the "Wiki system"

    * If the type is a "project" we talk about the "customer project" instead
      of the "customer system".

    * If the type is an "environment" we talk about the "staging environment"
      instead of the "staging system".

    This also reduces terminology issues where physical or virtual
    servers/machines may also be talked about as being "systems".

    Systems are created on an instance and may be federated. The instance that
    created them is considered the "primary" instance and has the highest
    authority on the data about a system.

    """

    __tablename__ = "system"

    category_id: Mapped[int] = mapped_column(
        ForeignKey("system_category.id"), init=False
    )
    category: Mapped[SystemCategory] = relationship(SystemCategory)

    primary_instance: Mapped[uuid.UUID]

    title: Mapped[str]

    # Subsystems are designed specifically as an n-to-m relation ship with the
    # idea that the subsystems itself should be quite independent and that this
    # is an organizational relationship for the UI that should be flexible.
    #
    # To avoid too many implicit dependencies on attributes from the parents
    # I'm currently not setting up the inverse relationship. We'll see how
    # this goes and whether this can hold over time.
    #
    # Also, the question is how this interacts with federation. I think
    # a federated system would also federate its subsystems but not it's
    # parents.
    #
    # That means we can't know whether other parent systems may exist
    # on remote systems that we federate to.
    subsystems: Mapped[list["System"]] = relationship(
        secondary=subsystem,
        primaryjoin="system.c.id == subsystem.c.system_id",
        secondaryjoin="system.c.id == subsystem.c.subsystem_id",
        default_factory=list,
    )
