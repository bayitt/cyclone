from fastapi import Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from .database import get_db
from ..schemas.application import ApplicationCreate, ApplicationUpdate
from ..database.models import Application
from ..utilities.exception import CycloneHTTPException


def create_application_pipe(body: ApplicationCreate, db: Session = Depends(get_db)):
    application = (
        db.query(Application).filter(Application.name == body.name.lower()).first()
    )

    if application:
        raise CycloneHTTPException(
            error="application-002",
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Application with name {body.name} exists already",
        )

    if body.credentials_type == 1:
        mailgun_keys = ["domain", "api_key", "from_name", "from_address"]
        invalidated_keys = list()

        for key in mailgun_keys:
            if not body.credentials_values.get(key):
                invalidated_keys.append(key)

        if len(invalidated_keys) > 0:
            raise CycloneHTTPException(
                error="credentials-003",
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{', '.join(invalidated_keys)} - missing from credentials values",
            )


def application_by_uuid_pipe(application_uuid: UUID, db: Session = Depends(get_db)):
    application = (
        db.query(Application).filter(Application.uuid == application_uuid).first()
    )

    if not application:
        raise CycloneHTTPException(
            error="application-001",
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with uuid {application_uuid} does not exist",
        )

    return application


def update_application_pipe(
    body: ApplicationUpdate,
    application: Application = Depends(application_by_uuid_pipe),
    db: Session = Depends(get_db),
):
    if body.name:
        named_application = (
            db.query(Application).filter(Application.name == body.name.lower()).first()
        )

        if named_application and named_application.uuid != application.uuid:
            raise CycloneHTTPException(
                error="application-002",
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Application with name {body.name} exists already",
            )

    return application
