from sqlalchemy import Column, ForeignKey, String, DateTime, Uuid, Integer, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid as uuid_pkg

from .setup import Base


class Application(Base):
    __tablename__ = "applications"

    uuid: uuid_pkg.UUID = Column(
        Uuid, default=uuid_pkg.uuid4, primary_key=True, index=True
    )
    name: str = Column(String, index=True)
    api_key: str | None = Column(String, nullable=True)
    layout: str | None = Column(String, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)

    credentials = relationship(
        "Credentials",
        back_populates="application",
        uselist=False,
    )
    emails = relationship(
        "Email",
        back_populates="application",
    )


class Credentials(Base):
    __tablename__ = "credentials"

    uuid: uuid_pkg.UUID = Column(
        Uuid, default=uuid_pkg.uuid4, primary_key=True, index=True
    )
    application_uuid: uuid_pkg.UUID = Column(
        Uuid, ForeignKey("applications.uuid", ondelete="CASCADE")
    )
    type: int = Column(Integer)
    values: dict[str, str] | None = Column(JSON, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)

    application = relationship(
        "Application", back_populates="credentials", passive_deletes=True
    )


class Email(Base):
    __tablename__ = "emails"

    uuid: uuid_pkg.UUID = Column(
        Uuid, default=uuid_pkg.uuid4, primary_key=True, index=True
    )
    application_uuid: uuid_pkg.UUID = Column(
        Uuid, ForeignKey("applications.uuid", ondelete="CASCADE")
    )
    name: str = Column(String, index=True)
    template: str = Column(String)
    variables: list[str] | None = Column(JSON, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)

    application = relationship(
        "Application", back_populates="emails", passive_deletes=True
    )
