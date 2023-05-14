from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

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
