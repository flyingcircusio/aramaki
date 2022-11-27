from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from aramaki.interfaces.sqlalchemy import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_id = Column(ForeignKey("systems.id"))
    system = relationship("System", back_populates="notifications")

    notified = Column(DateTime, nullable=True)
    concluded = Column(DateTime, nullable=True)
    qualification = Column(String(255))
    message = Column(String)
