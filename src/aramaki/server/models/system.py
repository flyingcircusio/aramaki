import uuid

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from . import meta


class System(meta.Base):
    __tablename__ = "system"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )

    title: Mapped[str]

    # Make this a dictionary, use references
    type_: Mapped[str]

    # XXX Turn into relationship
    primary_instance: Mapped[uuid.UUID]
