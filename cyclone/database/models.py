from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
    Uuid,
    SmallInteger,
    JSON,
    CHAR,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import uuid as uuid_pkg
from typing import Any

from .setup import Base
from ..utilities.jinja import parse_incoming_template, parse_outgoing_template


class Application(Base):
    __tablename__ = "applications"

    uuid: uuid_pkg.UUID = Column(
        Uuid, default=uuid_pkg.uuid4, primary_key=True, index=True
    )
    name: str = Column(String(50), index=True)
    api_key: str | None = Column(CHAR(32), nullable=True, index=True)
    _layout: str | None = Column(String, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @hybrid_property
    def layout(self):
        if not self._layout:
            return None

        return parse_outgoing_template(self._layout)

    @layout.setter
    def layout(self, layout: str | None):
        self._layout = None if not layout else parse_incoming_template(layout)

    credentials = relationship(
        "Credentials",
        back_populates="application",
        uselist=False,
    )
    emails = relationship(
        "Email",
        back_populates="application",
    )
    dispatches = relationship("Dispatch", back_populates="application")


class Credentials(Base):
    __tablename__ = "credentials"

    uuid: uuid_pkg.UUID = Column(
        Uuid, default=uuid_pkg.uuid4, primary_key=True, index=True
    )
    application_uuid: uuid_pkg.UUID = Column(
        Uuid, ForeignKey("applications.uuid", ondelete="CASCADE"), index=True
    )
    type: int = Column(SmallInteger)
    values: dict[str, str] | None = Column(JSON, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    application = relationship(
        "Application", back_populates="credentials", passive_deletes=True
    )


class Email(Base):
    __tablename__ = "emails"

    uuid: uuid_pkg.UUID = Column(
        Uuid, default=uuid_pkg.uuid4, primary_key=True, index=True
    )
    application_uuid: uuid_pkg.UUID = Column(
        Uuid, ForeignKey("applications.uuid", ondelete="CASCADE"), index=True
    )
    name: str = Column(String(100), index=True)
    subject: str = Column(String(100))
    _template: str = Column(String)
    variables: list[str] | None = Column(JSON, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @hybrid_property
    def template(self):
        return parse_outgoing_template(self._template)

    @template.setter
    def template(self, template: str):
        self._template = parse_incoming_template(template)

    application = relationship(
        "Application", back_populates="emails", passive_deletes=True
    )
    dispatches = relationship("Dispatch", back_populates="email")


class Dispatch(Base):
    __tablename__ = "dispatches"

    uuid: uuid_pkg.UUID = Column(
        Uuid, default=uuid_pkg.uuid4, primary_key=True, index=True
    )
    application_uuid: uuid_pkg.UUID = Column(
        Uuid, ForeignKey("applications.uuid", ondelete="CASCADE"), index=True
    )
    email_uuid: uuid_pkg.UUID = Column(
        Uuid, ForeignKey("emails.uuid", ondelete="CASCADE"), nullable=True
    )
    template: str = Column(String)
    variables: dict[str, Any] | None = Column(JSON, nullable=True)
    logs: str | None = Column(String, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    application = relationship(
        "Application", back_populates="dispatches", passive_deletes=True
    )
    email = relationship("Email", back_populates="dispatches")
