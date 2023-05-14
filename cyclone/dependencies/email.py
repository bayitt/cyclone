from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from ..database.models import Application, Email
from ..dependencies.application import application_by_uuid_pipe
from ..schemas.email import EmailCreate
from .database import get_db


def email_by_name_pipe(
    body: EmailCreate,
    application: Application = Depends(application_by_uuid_pipe),
    db: Session = Depends(get_db),
):
    email = (
        db.query(Email)
        .filter(
            Email.application_uuid == application.uuid, Email.name == body.name.upper()
        )
        .first()
    )

    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Application with uuid {application.uuid} already has email with name {body.name}",
        )


def email_by_uuid_pipe(email_uuid: UUID, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.uuid == email_uuid).first()

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Email with uuid {email_uuid} does not exist",
        )

    return email
