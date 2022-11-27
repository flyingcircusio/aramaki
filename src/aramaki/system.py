from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import relationship

from aramaki import context
from aramaki.interfaces.sqlalchemy import Base
from aramaki.notification import Notification


class System(Base):

    __tablename__ = "systems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)

    subsystems = relationship(
        "Subsystem",
        back_populates="system",
        cascade="all, delete-orphan",
    )
    notifications = relationship(
        "Notification",
        back_populates="system",
        cascade="all, delete-orphan",
    )

    actor_id = context.url("/systems/{name}")
    inbox_url = context.url("/systems/{name}/inbox")

    def use(self, id: str):
        subsystem = Subsystem.create(system=self, id=id)
        self.publish("Use", subsystem)

    @context.activitypub.receive(type="Use")
    def receive_usage_request(self, request):
        # XXX This could/should trigger a more elaborate workflow
        # who to accept or reject automatically or manually.
        self.used_by.append(request.actor)
        self.respond("Accept", request)

    # @context.activitypub.receive(type="Accept", object_type="Use"")
    def receive_usage_accepted(self, response):
        pass

    # @context.activitypub.receive(type="Reject", object_type="Use"")
    def receive_usage_rejected(self, response):
        pass

    def add_notification(self, message: str, qualification: str = "warning"):
        notification = Notification.create(
            message=message, qualification=qualification
        )
        self.notifications.append(notification)


class Subsystem(Base):

    __tablename__ = "subsystems"
    __table_args__ = (
        PrimaryKeyConstraint("system_id", "id"),
        {},
    )

    id = Column(String(255), nullable=False)
    system_id = Column(Integer, ForeignKey("systems.id"), nullable=False)
    system = relationship("System", back_populates="subsystems")

    @property
    def actor_id(self):
        return self.system_id

    # request_id = Column(Integer, ForeignKey("Activity.id"))
    # request = relationship("Activity", foreign_keys=[request_id])

    # response_id = Column(Integer, ForeignKey("Activity.id"))
    # response = relationship("Activity", foreign_keys=[response_id])

    approved = Column(Boolean)
