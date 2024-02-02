import uuid

from sqlalchemy import Column, String, func
from sqlalchemy.dialects.postgresql import UUID

from .meta import Base


class System(Base):
    __tablename__ = "system"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )

    title = Column(String, nullable=False)

    # Make this a dictionary.
    type_ = Column(String, nullable=False)

    # XXX Turn into relationship
    primary_instance = Column(UUID(as_uuid=True))
